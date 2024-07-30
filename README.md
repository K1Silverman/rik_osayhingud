# Osaühingud

* Backend ja frontend on eraldi kaustades
* Backendi jaoks kasutasin Python(3.10; pip 24.1.2) + Django(5.0.7)
* Frontendi jaoks kasutasin JavaScript(Node v20.14.0; npm 10.8.2) + Vue.js(3.4.29) + TailwindCSS
* Ma ei olnud kindel, kuidas isikute otsingus soovitakse andmeid source'ida, siis tekitasin 25 dummy FIEt migratsiooniga, mille seast otsitakse FIEsid. Kuna aega nappis, siis ei hakanud ka äriregistri API ligipääsu taotlema. Kui oleks aega rohkem olnud, siis oleks ka isikute osaga rohkem tegelenud.
* Lisaks aja nappuse tõttu jäi ka error handling küllaltki puiseks, mida saaks paremini teha.

## Backend

Open terminal
Move to backend directory

```sh
cd backend
```

### Project setup

```sh
pip install -r requirements.txt
```

### Backend server

1) Migrate SQLite db

```sh
python manage.py migrate
```

2) Run backend server (:8000)
```sh
python manage.py runserver
```


## Frontend

### Project Setup

Move to frontend directory

```sh
npm install
```

### Frontend server
Frontend server (:5173)
```sh
npm run dev
```