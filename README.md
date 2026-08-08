# Insights LLC — website

A static website for Insights LLC (Abby Stamelman Hocky, MSW). No build step, no
framework, no database: the files in this folder *are* the website. Open
`index.html` in a browser to see it exactly as visitors will.

```
index.html      the main (single) page
resume.html     the resume page
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

### 1. Create a GitHub account

Go to <https://github.com> and sign up if you don't already have an account.
Note the username you choose — it appears in the site's web address.

### 2. Create an empty repository

On GitHub, click **+** (top right) → **New repository**.

- **Repository name:** `insights-llc` (any name works; it shows up in the URL)
- **Public** — required for free GitHub Pages hosting
- Do **not** tick "Add a README file" — this folder already has one
- Click **Create repository**

### 3. Upload this folder

The simplest route, no software to install:

1. On the new repository's page, click **uploading an existing file**.
2. Open this `site` folder on your computer, select **everything inside it**
   (`index.html`, `resume.html`, `favicon.svg`, `README.md`, and the `css`,
   `js`, `images` and `fonts` folders) and drag it all onto the GitHub page.
   Upload the *contents* of the folder, not the folder itself — `index.html`
   must end up at the top level of the repository.
3. Scroll down and click **Commit changes**.

<details>
<summary>Or, if you prefer the command line</summary>

```bash
cd path/to/site
git init
git add .
git commit -m "Initial website"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/insights-llc.git
git push -u origin main
```

Run these from inside the `site` folder, so only the website files are in the
repository — the source documents in the parent folder stay off GitHub.
</details>

### 4. Turn on GitHub Pages

In the repository, go to **Settings** → **Pages** (left sidebar), then under
"Build and deployment":

- **Source:** Deploy from a branch
- **Branch:** `main`, folder `/ (root)`
- Click **Save**

Wait a minute or two, then reload the page. GitHub shows the live address:

```
https://YOUR-USERNAME.github.io/insights-llc/
```

That is the working website. Any time you change a file and commit it, the live
site updates within a minute or two.

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
   | CNAME | `www` | `YOUR-USERNAME.github.io.` |

3. Back in **Settings → Pages**, enter the domain under "Custom domain", save,
   and tick **Enforce HTTPS** once it becomes available (usually within an hour).

GitHub's own instructions, if you want a second opinion:
<https://docs.github.com/pages/configuring-a-custom-domain-for-your-github-pages-site>

---

## Part 2 — Updating the site later

Everything a visitor reads lives in `index.html` and `resume.html`. You can edit
those two files directly on GitHub (open the file, click the pencil icon, make
the change, click **Commit changes**) and the live site updates itself.

### Changing words

Open `index.html`. It is marked with comments like

```html
<!-- ===================== WELCOME ===================== -->
```

so you can find the part you want. Text sits between tags — change only the
words, and leave the tags on either side alone:

```html
<h2>Spiritual Accompaniment</h2>
     ↑ change this ↑
```

A few things worth knowing:

- `<p>…</p>` is one paragraph. To add another, copy an existing pair of tags.
- `<strong>…</strong>` makes text bold; `<em>…</em>` makes it italic.
- The bullet points inside the cards are `<li>…</li>` lines — copy a whole line
  to add another bullet, or delete a line to remove one.
- The email address and phone number appear in three places on the main page
  (the contact band and the footer) and twice on the resume page. Search for
  `abbysh` and `215-839` to catch them all.

### Changing a photograph

Put the new picture in the `images` folder and update the filename in the HTML,
for example:

```html
<img src="images/rocks.jpg" alt="Smooth beach stones of many colours resting together" …>
```

Keep the `alt` text accurate — it is what people using a screen reader hear, and
what shows if the image fails to load. Photos straight from a phone are much
larger than a website needs; resizing them to about 1,600 pixels wide before
uploading keeps the site quick.

The photographs currently in use:

| File           | Where it appears                          |
|----------------|-------------------------------------------|
| `ocean.jpg`    | Background of the top banner              |
| `headshot.jpg` | Portrait in the welcome section           |
| `lake.jpg`     | Spiritual Accompaniment card              |
| `rocks.jpg`    | Leadership & Organizational Consulting card |
| `sunset.jpg`   | Background of the contact band            |
| `flower.jpg`   | Background of the resume page heading     |

### Changing colours or type

`css/styles.css` begins with a short list of the site's colours:

```css
--sand:      #f6f2ea;   /* page background */
--clay:      #9a4f35;   /* accent: links, rules */
```

Change a value there and it changes everywhere it is used. The rest of the
stylesheet is grouped into numbered, labelled sections.

### Checking your work

After committing a change, wait a minute, then reload the live site — a "hard"
reload (Shift + reload) makes sure you are not looking at a cached copy. It is
worth glancing at the site on a phone too; the layout rearranges itself for
narrow screens.

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
