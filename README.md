# Insights LLC — website

A static website for Insights LLC (Abby Stamelman Hocky). No framework and
no database: the files in this folder *are* the website. Open `index.html` in a
browser to see it exactly as visitors will.

```
content.md      ← the words on the main page. This is the file to edit.
index.html      the main page, BUILT from content.md — don't edit by hand
_template.html  the structure of the main page (layout, not words)
build.py        turns content.md + _template.html into index.html

bio.html        the bio page, edited directly as HTML
resume.html     the resume page, edited directly as HTML
css/styles.css  all of the styling, in labelled sections
css/fonts.css   the two web fonts, stored in this folder
js/main.js      the card-flipping behaviour and the footer year
images/         photographs used on the site
fonts/          Lora and Inter (open-source, SIL Open Font License)
favicon.svg     the little icon shown in a browser tab
tools/          one optional script, for redrawing the sharing preview card
CNAME           the site's address, ash-insights.com — see Part 1, section 5
```

Everything the site needs is in this folder — it loads nothing from any other
company's servers, so it will keep working, and load quickly, indefinitely.

---

## Part 1 — Putting the site on the web with GitHub Pages

GitHub Pages hosts static sites like this one for free. Do this once.

### 1. Before you start

You need a GitHub account that is a member of the `insights-llc` organization,
and git on your computer (macOS: `git --version` in Terminal will offer to
install it if it is missing).

### 2. The repository

The site pushes to:

```
git@github.com:insights-llc/insights-llc.github.io.git
```

Because the repository is named `insights-llc.github.io`, GitHub treats it as
the organization's main site and serves it from the root address:

```
https://insights-llc.github.io/
```

That is the address GitHub gives away free. The site's real address is
**<https://ash-insights.com>**, which is section 5 below; the GitHub one keeps
working and redirects to it.

### 3. Push this folder

This folder is already a git repository with the site committed, and the remote
is already set. From a Terminal window:

```bash
cd path/to/site
git push -u origin main
```

That first push needs an SSH key that has access to the `insights-llc`
organization — the same key you use for any other GitHub repository. If SSH is
not set up on this machine, use the HTTPS address instead:

```bash
git remote set-url origin https://github.com/insights-llc/insights-llc.github.io.git
git push -u origin main
```

After the first push, publishing a change is just `git push` (or, for text
edits, the browser route described in Part 2).

### 4. Check GitHub Pages is on

For a repository named `username.github.io` or `orgname.github.io`, Pages is
usually switched on by itself. Confirm it under **Settings → Pages**:

- **Source:** Deploy from a branch
- **Branch:** `main`, folder `/ (root)`

Give it a minute or two after the first push, then visit
<https://insights-llc.github.io/>.

Two settings worth checking once, under **Settings → Actions → General**,
because the automation in Part 2 commits the rebuilt page back to the
repository: **Workflow permissions** should be set to *Read and write
permissions*.

### 5. Pointing ash-insights.com at the site

The address of the site is **ash-insights.com**, registered at Hover. Two
things have to agree for that to work: GitHub has to know the site answers to
that name, and Hover has to send visitors to GitHub's servers.

**The GitHub half is already done.** The file named `CNAME` in this folder
contains one line, `ash-insights.com`, and that is what tells GitHub. Do not
delete or rename it; a stray edit to that file takes the site off the air.

**The Hover half** is a one-time change, done at
[hover.com](https://www.hover.com) → sign in → **ash-insights.com** → the
**DNS** tab.

A new domain arrives with placeholder records pointing at Hover's own "parked"
page. Those have to go, or they will keep winning:

1. **Delete** every existing `A` record whose name is `@`, and the existing
   `CNAME` record named `www`. Leave anything else alone — in particular leave
   `MX` records alone, since those carry email.
2. **Add** these five records. Hover asks for a Type, a Hostname and a Value;
   the TTL can stay at whatever it offers.

   | Type  | Hostname | Value                   |
   |-------|----------|-------------------------|
   | A     | `@`      | `185.199.108.153`       |
   | A     | `@`      | `185.199.109.153`       |
   | A     | `@`      | `185.199.110.153`       |
   | A     | `@`      | `185.199.111.153`       |
   | CNAME | `www`    | `insights-llc.github.io` |

   Four `A` records is correct, not a mistake — they are GitHub's four servers,
   and the site will use whichever answers first. The `CNAME` is what makes
   `www.ash-insights.com` work as well as the bare name; GitHub redirects one
   to the other by itself.

3. **Wait.** The change usually takes effect within an hour, occasionally
   longer. Meanwhile the site stays reachable at its GitHub address.
4. Once <https://ash-insights.com> loads, go to **Settings → Pages** in the
   repository and tick **Enforce HTTPS**. That option only becomes available
   after GitHub has issued a certificate for the domain, which takes a few
   minutes more. Tick it — it is what makes the padlock appear in the browser.

To check progress from a Terminal without waiting on the browser:

```bash
dig +short ash-insights.com
```

Once that prints the four `185.199.*` addresses instead of anything else, the
change has gone through.

GitHub's own instructions, if you want a second opinion:
<https://docs.github.com/pages/configuring-a-custom-domain-for-your-github-pages-site>

---

## Part 2 — Changing the words on the main page

**Everything a visitor reads on the main page lives in `content.md`.** It is
plain text with a little light mark-up, and it is the only file you need for
ordinary edits. `index.html` is built from it and is overwritten each time, so
never edit `index.html` directly.

### The easy way: edit on GitHub, in a browser

1. Open the repository on github.com and click `content.md`.
2. Click the pencil icon (**Edit this file**).
3. Change the words.
4. Scroll down and click **Commit changes**.

That is all. A small automation in this repository notices the change, rebuilds
`index.html`, and publishes it; the live site catches up within a couple of
minutes. If you want to watch it happen, the **Actions** tab shows the run.

### The other way: edit on your own computer

Edit `content.md` in any text editor, then rebuild the page:

```bash
python3 build.py
```

The first time only, install the one library it needs:

```bash
pip install markdown      # some Macs need: pip3 install markdown
```

Then open `index.html` to check it, and commit both `content.md` and
`index.html`.

> On Greg's Mac this is already set up in the `Python39` conda environment,
> which is where the local builds have been run from:
>
> ```bash
> /Users/hockyg/Software/miniconda3/envs/Python39/bin/python build.py
> ```

### What content.md looks like

The top of the file, between two rows of dashes, is a list of short settings —
one per line, in the form `name: value`. Change what comes after the colon and
leave the name alone. That is where the email address, the phone number, the
headline, the photo filenames and the browser-tab title live.

One thing is deliberately *not* there: the "Insights LLC" wordmark, in the
header and again beneath Abby's name. It is set as a small piece of design
rather than as a line of text — italic *Insights* followed by spaced capitals —
so it lives in `_template.html`, `bio.html` and `resume.html`, and all four
places are meant to change together.

Below that come the longer passages, each under a heading like `## Welcome` or
`## Card one — back`. **Keep those headings exactly as they are** — the page is
assembled from them — and change only the writing underneath.

Within the writing:

- A blank line starts a new paragraph.
- `**Text in double asterisks**` comes out **bold**, `*single asterisks*`
  *italic*.
- A line starting with `- ` becomes a bullet point.
- `[Words in square brackets](https://example.com)` become a link.
- A line starting with `### ` becomes a small heading inside a card.
- A line starting with `> ` becomes the note set off by a coloured rule — the
  one about fees. A `> #### Fees` line at the top of it becomes the small
  capitals heading on that note.

If you mistype a heading or delete a setting, `build.py` stops and says exactly
what is missing rather than publishing a broken page.

---

## Part 3 — Everything else

### The bio and resume pages

`bio.html` and `resume.html` are ordinary HTML, edited directly rather than
built from `content.md`. On the bio page the writing sits in three plain
paragraphs; change the words between `<p>` and `</p>` and leave the tags alone.

On the resume page the entries follow a repeating pattern, so the simplest way
to add one is to copy an existing block and change the words inside it:

```html
<li>
  <p class="entry__title">Name of the award or role</p>
  <p class="entry__meta">Organization, year</p>
</li>
```

Both pages, and the main page, carry a short list of links across the top. If a
page is ever added or renamed, that list has to be corrected in three places:
`_template.html` (for the main page), `bio.html` and `resume.html`.

#### Saving either page as a PDF

Both pages end with a **Save as PDF** button. It opens the browser's own print
dialog, where *Save as PDF* is one of the destinations — so the file is made by
the browser, and there is no separate PDF on the site to keep up to date. What
comes out is a plain document: the name and wordmark as a letterhead, a
hairline under it, then the writing, and on the bio page the portrait beside
it. The navigation, the buttons, the footer and the background photographs all
drop away.

The button is hidden if JavaScript is unavailable; Print in the browser's own
menu does exactly the same thing.

---

### The preview card

When the address of the site is texted, posted in Slack, or pasted into
Facebook or LinkedIn, the app quietly fetches the page and builds a small card
out of hidden tags in it — a picture, a title and a line of description. The
main page's card comes from five settings at the top of `content.md`:

```
site_url:            https://ash-insights.com
preview_image:       images/social-card.jpg
preview_title:       Insights LLC — Abby Stamelman Hocky
preview_description: Leadership and organizational consulting, and spiritual …
preview_alt:         Dune grass above a calm sea, above the words …
```

Three things are worth knowing:

- **`site_url` has to be right.** The picture is sent to messaging apps as a
  full web address, which is worked out from this setting. If the site later
  moves to its own domain name, change `site_url` the same day, or the preview
  will quietly stop appearing.
- **The picture should be 1200 × 630 pixels.** That is the shape every app
  expects; anything else gets cropped unpredictably, and small pictures are
  ignored altogether. `build.py` prints a note if the file is a different size,
  and stops outright if it is missing.
- **Messages shows only the picture and a short title.** The description is for
  Slack, WhatsApp, Facebook and LinkedIn. Apple also tends to shorten the title,
  which is why the picture itself carries the business name.

To use a different picture, put it in the `images` folder and point
`preview_image` at it, then rebuild. `bio.html` and `resume.html` have the same
tags written into them directly, near the top of each file, so change those too
if the picture is meant to be the same everywhere.

#### Why a change may not show up

Every one of these apps caches previews, and Messages in particular remembers
what it saw more or less indefinitely. A card someone has already received will
not change.

- **Give a replacement picture a new filename** — `social-card-2.jpg` rather
  than a new version of `social-card.jpg`. This is the one reliable way to make
  the change stick.
- To see what the apps are reading now, paste the address into Facebook's
  [sharing debugger](https://developers.facebook.com/tools/debug/), which has a
  *Scrape Again* button, or LinkedIn's
  [post inspector](https://www.linkedin.com/post-inspector/).
- To test in Messages without waiting, add something harmless to the end of the
  address — `https://ash-insights.com/?v=2` — which the site ignores but
  which Messages treats as a new page.

#### Redrawing the branded card

`images/social-card.jpg` — the sea, the wordmark and the name — is drawn by
`tools/make-social-card.py`, using the site's own fonts and colours. It is
committed to the repository, so this only needs running if the wording on the
card should change. Unlike `build.py` it needs three extra libraries:

```bash
pip install pillow fonttools brotli
python3 tools/make-social-card.py
```

The words it draws are constants near the top of that file. Nothing else on the
site depends on it.

### Changing a photograph

Put the new picture in the `images` folder, then point at it from `content.md`
(for the main page) or from `resume.html`. In `content.md` that means changing a
line such as:

```
card_one_image: images/lake.jpg
card_one_alt: A hammock strung between trees above a lake at dusk
```

Keep the `alt` description accurate — it is what someone using a screen reader
hears, and what shows if the image fails to load. Photos straight from a phone
are much larger than a website needs; resizing them to about 1,600 pixels wide
before adding them keeps the site quick.

The photographs currently in use:

| File              | Where it appears                                   |
|-------------------|----------------------------------------------------|
| `ocean.jpg`       | Background of the top banner                       |
| `headshot.jpg`    | Portrait in the welcome section, and on the bio page |
| `lake.jpg`        | Spiritual Accompaniment card; bio page heading     |
| `rocks.jpg`       | Leadership & Organizational Consulting card        |
| `sunset.jpg`      | Background of the contact band                     |
| `flower.jpg`      | Background of the resume page heading              |
| `social-card.jpg` | The sharing preview — see "The preview card" above |

### Changing colours or type

`css/styles.css` begins with a short list of the site's colours:

```css
--sand:      #f6f2ea;   /* page background */
--clay:      #9a4f35;   /* accent: links, rules */
```

Change a value there and it changes everywhere it is used. The rest of the
stylesheet is grouped into numbered, labelled sections.

### Checking your work

After committing a change, wait a minute or two, then reload the live site — a
"hard" reload (Shift + reload) makes sure you are not looking at a cached copy.
It is worth glancing at the site on a phone too; the layout rearranges itself
for narrow screens.

---

## Notes on how it was built

- **The two service cards flip.** Selecting a card (or its "Read more" button)
  turns it over to reveal the full description. If JavaScript is unavailable,
  the cards simply show all of their text at once, so nothing is ever hidden
  from a visitor or from a search engine.
- **Accessibility.** The cards can be operated by keyboard, the hidden side of a
  card is kept out of the tab order, colours meet WCAG AA contrast, and the
  layout responds to a "reduce motion" preference.
- **The resume page prints cleanly** — navigation, buttons and background images
  drop away when someone chooses Print or "Save as PDF".
- **Why index.html is committed even though it is generated.** Keeping it in the
  repository means the site still works if the automation is ever turned off,
  and that double-clicking `index.html` on your own computer previews the real
  page without building anything first.
