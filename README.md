# Zettelkasten for BBEdit

A lightweight knowledge management system using BBEdit and Markdown files, with support for:

- **LaTeX math** via MathJax (`$...$` for inline, `$$...$$` for display)
- **Wiki-links** (`[[Note Name]]`) that open linked notes in BBEdit
- **Zotero citations** (`[[@citekey]]`) that open papers in Zotero
- **Tags** (`#tag-name`) rendered with distinct styling
- **Images, hyperlinks, and standard Markdown** rendered in BBEdit's preview
- **Dollar sign protection** so `$500` isn't mistaken for math

No databases, no Electron apps, no syncing services — just Markdown files on your filesystem and BBEdit's built-in preview.

## Installation

```bash
git clone https://github.com/robertoabraham/zettelkasten-bbedit.git
cd zettelkasten-bbedit
./install.sh
```

This will:
1. Install the `Zettelkasten.bbpackage` into BBEdit's Packages folder
2. Create `~/Zettelkasten` if it doesn't already exist
3. Install the backlinks helper script into `~/Zettelkasten/.scripts/`

To uninstall: `./install.sh --uninstall`

## Usage

1. Create `.md` files in `~/Zettelkasten`
2. Open a file in BBEdit and choose **Markup > Preview in BBEdit**
3. In the preview toolbar, set **Template** to **Zettelkasten.html**
4. Write math, wiki-links, and standard Markdown as usual

### Math

Use `$...$` for inline math and `$$...$$` for display math:

```markdown
The solution is $x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}$.

$$\nabla \times \mathbf{B} = \mu_0 \mathbf{J}$$
```

Dollar signs followed by digits (e.g., `$500`) are automatically protected and will not be treated as math delimiters.

### Wiki-Links

Link between notes with double brackets:

```markdown
See also [[Another Note]] and [[Subfolder/Deep Note]].
```

Clicking a wiki-link in the preview opens the target `.md` file in BBEdit.

### Zotero Citations

Reference papers in your Zotero library using `[[@citekey]]` syntax:

```markdown
See [[@allen2008]] for the MAPPINGS III models.
```

Clicking a citation link opens the paper in Zotero (requires the Better BibTeX plugin).

### Tags

Add tags to your notes with `#tag-name`:

```markdown
This note is about #stellar-evolution and #spectroscopy.
```

Tags are rendered with a distinct orange style in the preview. They won't conflict with Markdown headings (which use `# ` with a space).

### Images and Links

Standard Markdown images and links work normally:

```markdown
![Photo](images/photo.png)
[Paper](https://www.zotero.org/groups/...)
[Local PDF](</path/to/file with spaces.pdf>)
```

For file paths containing parentheses or spaces, wrap the URL in angle brackets: `(<path>)`.

### Backlinks

Find all notes that reference the current note:

```bash
python3 ~/Zettelkasten/.scripts/find_backlinks.py /path/to/note.md
```

## Customization

### Notes folder location

If your notes live somewhere other than `~/Zettelkasten`, edit the `ZETTELKASTEN_ROOT` variable near the top of the preview template:

```javascript
var ZETTELKASTEN_ROOT = '~/Zettelkasten';  // change this
```

The template is located at:
`~/Library/Application Support/BBEdit/Packages/Zettelkasten.bbpackage/Contents/Preview Templates/Zettelkasten.html`

## Repository Structure

```
zettelkasten-bbedit/
  Zettelkasten.bbpackage/     BBEdit package (drop into Packages folder)
    Contents/
      Preview Templates/
        Zettelkasten.html     MathJax + wiki-links preview template
      Preview CSS/
        zettelkasten.css      Centered, readable-width layout
        zettelkasten-wide.css Full-width variant
  scripts/
    find_backlinks.py         Backlink finder utility
  examples/
    Math Preview Test.md      Test file demonstrating all features
  install.sh                  Installer / uninstaller
  README.md
```

## Requirements

- macOS
- [BBEdit](https://www.barebones.com/products/bbedit/) (14+)
- Internet connection (MathJax is loaded from CDN)
