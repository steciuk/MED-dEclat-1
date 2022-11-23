# Przydatne komendy

## Windows
Tworzenie środowiska wirtualnego

```
py -3 -m venv .venv
```

Aktywowanie środowiska wirtualnego

```
.venv\scripts\activate
```

Dezaktywowanie środowiska wirtualnego

```
deactivate
```

Zainstalowanie wszystkich zależności zapisanych w [requirements.txt](requirements.txt)

```
python -m pip install -r requirements.txt
```

Instalacja nowej zależności

```
python -m pip install <package_name>
```

Zapisanie wszystkich zainstalowanych zależności do [requirements.txt](requirements.txt)

```
python -m pip freeze > requirements.txt
```

Uruchomienie testów

```
python -m pytest
```

## macOS/Linux
Tworzenie środowiska wirtualnego

```
python3 -m venv .venv
```

Aktywowanie środowiska wirtualnego

```
source .venv/bin/activate
```

Reszta tak jak dla Windows ze zmianą `python` na `python3`