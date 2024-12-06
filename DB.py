import sqlite3

con = sqlite3.connect('biblio.db')
cursor = con.cursor()

# Aircraft Table
cursor.execute("""
   CREATE TABLE IF NOT EXISTS aircraft (
    NUMAV INTEGER PRIMARY KEY NOT NULL,
    TYPE VARCHAR(200) NOT NULL,
    datems DATE NOT NULL,
    NBHDDREV INTEGER DEFAULT 0,
    status TEXT NOT NULL CHECK (status IN ('Available', 'In Maintenance', 'Out of Service'))
)
""")

# Employees Table
cursor.execute("""
  CREATE TABLE IF NOT EXISTS employees (
    NUMEMP INTEGER PRIMARY KEY NOT NULL,
    NOM TEXT NOT NULL,
    prenom TEXT,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,                      
    tel INTEGER,
    ville TEXT NOT NULL,
    adresse TEXT NOT NULL,
    salaire FLOAT NOT NULL,
    FONCTION TEXT NOT NULL,
    datemb DATE NOT NULL,
    NBMHV INTEGER DEFAULT 0,
    NBTHV INTEGER DEFAULT 0
)
""")

# Revision Table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS revision (
    NUMREV INTEGER PRIMARY KEY NOT NULL,
    RAPPPORT TEXT NOT NULL,
    DATEREV DATE NOT NULL,
    NBHREV INTEGER NOT NULL,
    NUMAV INTEGER NOT NULL,
    TECID INTEGER DEFAULT -1, 
    FOREIGN KEY(NUMAV) REFERENCES aircraft(NUMAV),
    FOREIGN KEY(TECID) REFERENCES employees(NUMEMP) ON DELETE SET DEFAULT
)
""")

# Airport Table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS airport (
        CODEV CHAR(3) PRIMARY KEY NOT NULL,
        NOM VARCHAR(50) NOT NULL,
        Pays VARCHAR(50) NOT NULL,
        VILLE VARCHAR(50) NOT NULL
    )
""")

# Escale Table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS escale (
        IDESC INTEGER PRIMARY KEY NOT NULL,
        APORTESC VARCHAR(3) NOT NULL,
        HARMESC TIME NOT NULL,
        DURESC TIME NOT NULL,
        NOORD INT NOT NULL,
        NUMVOL INTEGER NOT NULL,
        FOREIGN KEY (NUMVOL) REFERENCES vol(NUMVOL) ON DELETE CASCADE,
        FOREIGN KEY (APORTESC) REFERENCES airport(CODEV) ON DELETE CASCADE
    )
""")

# Vol Table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS vol (
    NUMVOL INTEGER PRIMARY KEY NOT NULL,
    APORTDEP VARCHAR(255) NOT NULL,
    APORTARR VARCHAR(255) NOT NULL,
    HDEP TIME NOT NULL,
    durvol INTEGER NOT NULL,
    jvol TEXT NOT NULL CHECK (jvol IN ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')),
    FOREIGN KEY(APORTDEP) REFERENCES airport(CODEV) ON DELETE CASCADE,
    FOREIGN KEY(APORTARR) REFERENCES airport(CODEV) ON DELETE CASCADE,
    FOREIGN KEY (NUMVOL) REFERENCES aircraft(NUMAV) ON DELETE RESTRICT
)
""")

# Employee-Vol Table (Many-to-Many Relationship)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS employee_vol (
    NUMEMP INTEGER NOT NULL,
    NUMVOL INTEGER NOT NULL,
    PRIMARY KEY (NUMEMP, NUMVOL),
    FOREIGN KEY (NUMEMP) REFERENCES employees(NUMEMP) ON DELETE CASCADE,
    FOREIGN KEY (NUMVOL) REFERENCES vol(NUMVOL) ON DELETE CASCADE
)
""")

# Commit and close connection
con.commit()
con.close()
