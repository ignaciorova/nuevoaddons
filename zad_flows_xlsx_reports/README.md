# Zad Flows - XLSX Report Generator

Generate Excel (XLSX) reports from Jinja-powered templates stored in Odoo.

## Key features
- Store XLSX templates per model
- Render cell text with Jinja expressions (e.g., `{{ docs.name }}`)
- Built-in helpers: `spelled_out()`, `formatdate()`, `convert_currency()`
- Image tag: `{% img docs.image_1920 %}` to place a binary image onto the worksheet at the tag cell
- Wizard to generate a report for the active record
- Example template for `res.partner`

## How it works
1. Create a **Template** (Settings → Zad Flows → XLSX Reports → Templates), choose a model and upload an `.xlsx` file with placeholders.
2. Link a template to a report action or use the **Export XLSX** wizard from any record via the action menu.
3. Download the generated spreadsheet.

## Placeholder examples
- Text: `{{ docs.name }}`
- Date formatting: `{{ formatdate(docs.create_date, '%d-%m-%Y') }}`
- Numbers in words: `{{ spelled_out(1250) }}`
- Currency rounding: `{{ convert_currency(123.456, docs.company_currency_id) }}`
- Image: `{% img docs.image_1920 %}`

This module is an original implementation by **Zad Flows**.
