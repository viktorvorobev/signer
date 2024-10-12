# PDF Signer

Tool to sign workhours stuff in Hungarian companies

## How to use

> [!warning]
> It is a first prototype after all.

1. Create an image of your signature with transparent background (e.g. use [this tool](https://www.adobe.com/express/feature/image/remove-background/png/transparent))
2. Download this project
3. Create virtual python environment:
    ```bash
    python3 -m venv .venv
    ```
4. Activate environment:
    ```bash
    source .venv/bin/activate
    ```
5. Install dependencies
    ```bash
    pip install -e .
    ```
6. Tweak info at the end of the `src/signer/pdf_creator.py`
    - Check your name
    - Path to the signature
    - Public holiday dates
    - Your vacation dates
7. Run script
    ```bash
    python3 ./src/signer/pdf_creator.py 
    ```
