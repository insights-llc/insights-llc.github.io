# Insights LLC — website

A static website for Insights LLC (Abby Stamelman Hocky, MSW). No framework and
no database: the files in this folder *are* the website. Open `index.html` in a
browser to see it exactly as visitors will.

```
content.md      ← the words on the main page. This is the file to edit.
index.html      the main page, BUILT from content.md — don't edit by hand
_template.html  the structure of the main page (layout, not words)
build.py        turns content.md + _template.html into index.html

resume.html     the resume page, edited directly as HTML
css/styles.css  all of the styling, in labelled sections
css/fonts.css   the two web fonts, stored in this folder
js/main.js      the card-flipping behaviour and the footer year
images/         photographs used on the site
fonts/          Lora and Inter (open-source, SIL Open Font License)
favicon.svg     the little icon shown in a browser tab
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

### 5. (Optional) Use your own domain name

The draft mentioned securing a web address with "insights" in it. Once you have
bought one from a registrar such as Namecheap, Porkbun, Cloudflare or Google
Domains:

1. In the repository, create a file named `CNAME` (no extension) containing only
   your domain, e.g. `insightsconsultingllc.com`
2. At your registrar, point the domain at GitHub by adding these DNS records:

   | Type  | Name  | Value                    |
   |-------|-------|--------------------------|
   | A     | `@`   | `185.199.108.153`        |
   | A     | `@`   | `185.199.109.153`        |
   | A     | `@`   | `185.199.110.153`        |
   | A     | `@`   | `185.199.111.153`        |
   | CNAME | `www` | `insights-llc.github.io.` |

3. Back in **Settings → Pages**, enter the domain under "Custom domain", save,
   and tick **Enforce HTTPS** once it becomes available (usually within an hour).

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

### What content.md looks like

The top of the file, between two rows of dashes, is a list of short settings —
one per line, in the form `name: value`. Change what comes after the colon and
leave the name alone. That is where the email address, the phone number, the
headline, the photo filenames and the browser-tab title live.

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
- A line starting with `> ` becomes the highlighted note about fees.
- Anything after a line of three dashes at the end of a card becomes the small
  footnote text.

If you mistype a heading or delete a setting, `build.py` stops and says exactly
what is missing rather than publishing a broken page.

---

## Part 3 — Everything else

### The resume page

`resume.html` is ordinary HTML, edited directly. The entries follow a repeating
pattern, so the simplest way to add one is to copy an existing block and change
the words inside it:

```html
<li>
  <p class="entry__title">Name of the award or role</p>
  <p class="entry__meta">Organization, year</p>
</li>
```

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

| File           | Where it appears                            |
|----------------|---------------------------------------------|
| `ocean.jpg`    | Background of the top banner                |
| `headshot.jpg` | Portrait in the welcome section             |
| `lake.jpg`     | Spiritual Accompaniment card                |
| `rocks.jpg`    | Leadership & Organizational Consulting card |
| `sunset.jpg`   | Background of the contact band              |
| `flower.jpg`   | Background of the resume page heading       |

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
