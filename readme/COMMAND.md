## Create a directory with file

```bash
mkdir -p apps && touch apps/__init__.py
```

## Create a Directory inside a directory with file

```bash
mkdir -p apps/common && touch apps/common/__init__.py
```

## Create a Django App inside apps directory

```bash
python manage.py startapp common apps/common
```
