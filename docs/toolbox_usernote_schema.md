# Toolbox Usernotes Wiki Page

Unofficial documentation. Canonnical documentation may be found 
[here](https://github.com/toolbox-team/reddit-moderator-toolbox/wiki/Subreddit-Wikis%3A-usernotes).

Moderator Toolbox stores usernotes at `https://reddit.com/r/{sub}/wiki/usernotes`,
where `{sub}` is the name of a subreddit. The wiki is stored as a plain JSON object
with the following properties (indicated as python types after loading the JSON):

ver \[Integer\]
: The Usernotes format version. The current version of the usernotes page is `6`.
Increases in the version number indicate breaking changes to this schema; a 
lower version of this schema should *never* be written back to the wiki.

constants \[Dictionary\]
: A misnomer, as data in this section is entirely mutable; the only thing which
should remain constant is the order of existing values in each respective list.
: users \[List\]
	: a misnomer - this is a list of *moderator* usernames (without the leading
	 "/u/", e.g. "adhesiveCheese") who have left notes for users, not users with
	 notes as the name might lead you to believe. Each individual note maps the
	 `m` key as an index of this array; as such, you cannot modify the order of
	 or remove members from this list without updating every single usernote. 
	 New entries in this list should always be added to the end of the list.
: warnings \[List\]
	: a list of note type names as strings. just like with the `users` list, you
	cannot modify the order of or remove items from this list without updating 
	every single usernote. These strings correspond to the `key` item for each 
	dictionary in the `usernoteColors` in the Toolbox settings schema. Only 
	warning types which appear in at least one note exist in this list, even if 
	additional note types are configured in settings.
: blob \[String\]
	A zlib-compressed, base64-encoded string that, when decoded and 
	decompressed, gives a JSON object containing all usernotes. For working with
	notes, this blob is decompressed and replaced with `users`, which is 
	described in the next section

Example of this schema, with the blob portion replaced with it's expanded `users`
key:

<details>
<summary>Click to view</summary>

```json
{
   "ver":6,
   "constants":{
      "users":["adhesiveCheese"],
      "warnings":["gooduser"]
   },
   "users":{
      "sirensie":{
         "ns":[
            {
               "n":"Fiesty",
               "t":1583939357,
               "m":0,
               "l":"l,fcxy4s",
               "w":0
            }
         ]
      }
   }
}
```
</details>
<br>

## Users

Users is a dictionary. Each key is the name of a user (without `/u/`, as with 
moderators earlier) who has usernotes. This dictionary has exactly one key, `ns`, 
which is a list of dictionaries each representing a [single note](#note).

It is important to keep in mind that JSON keys are case-sensitive; 
`adhesivecheese` and `adhesiveCheese` are two seperate keys.

## Note

A note is a dictionary.

t \[Integer\]
: The unix timestamp of the notes creation; the number of seconds sinc the 
epoch (1970-01-01 00:00 UTC).

n \[String\]
: The text of the usernote.

m \[integer\]
: The index of the moderator who added the note; index starts at 0. Determined 
from the `users` section in `constants`.

w \[integer\]
: The index of the warning key; index starts at 0. Determined from the 
`warnings` section in `constants`.

l \[String\] (lower-case L, not 1 or capital i)
: This key may not exist on all notes. A string representing a link to where 
the note was added from. Toolbox compresses Submission, Comment, and old modmail
links, so you should not assume this link is a valid URL. Link string formats
are discussed in the next section.

## Links

To save space, Toolbox avoids storing full URLs in usernotes when it can. 
Instead, shorthand formats are used and converted into full URLs when read. In 
the following examples, things in `{Curly Brackets}` are stand-ins for 
substrings; all other characters are literal.

`l,{SUBMISSION_ID},{COMMENT_ID}`
: Represents a link to a comment. May be expanded to 
`https://reddit.com/comments/{SUBMISSION_ID}/-/{COMMENT_ID}`

`l,{SUBMISSION_ID}`
: Represents a link to a submission. May be expanded to 
`https://reddit.com/{SUBMISSION_ID}`

`m,{THREAD_ID}`
: Represents an old modmail link. May be expanded to 
`https://www.reddit.com/message/messages/{THREAD_ID}`

Others
: All other links (such as new modmail) are stored as full urls. Writing full 
URLs other than new modmail permalinks is discouraged—don't introduce external 
URLs, and use the shorthand formats for other resources on Reddit. However, for 
legacy support, you should support reading arbitrary URLs (not just new modmail 
links), and convert them to the shorthand formats when applicable.
