Power BI Project (.pbip) Templates for Experiments 1-8
======================================================

Why .pbip instead of pre-compiled .pbix?
Microsoft .pbix archives embed a proprietary binary XPress9-compressed VertiPaq
DataModel and Windows DPAPI-encrypted SecurityBindings that only Power BI Desktop's
internal Save engine can emit.

How to open and save as .pbix in one click:
1. Open any Exp0X_.../*.pbip file directly in Microsoft Power BI Desktop (>= v2.130).
2. Click 'Refresh' if prompted to load the CSV from ../Datasets/.
3. Click File -> Save As -> Power BI file (*.pbix) if you need a single-file .pbix export.
