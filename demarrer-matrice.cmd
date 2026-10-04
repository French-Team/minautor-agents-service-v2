@echo off
REM ==========================================================================
REM  demarrer-matrice.cmd -- LE PREMIER GESTE, et le seul qui ne soit pas Python.
REM ==========================================================================
REM
REM  POURQUOI CE FICHIER EXISTE, ET POURQUOI IL EST EN BATCH.
REM
REM  Le premier geste du projet etait :
REM      python3 cerveau-projet/matrix/lancer.py ...
REM  Ce geste suppose que Python existe DEJA -- donc il ne peut, jamais, constate
REM  que Python manque. Un garde ecrit en Python est muet precisement quand il
REM  serait necessaire (defaut deja vu dans ce depot : commun.py de
REM  editer-agents-md, qui appelait detecter_racine sans l importer -- NameError
REM  a la premiere utilisation, la porte ne pouvait plus rien faire).
REM
REM  Le livrable est sans Python (63 Mo de sources, le runtime pese 23 Mo et
REM  n est pas versionne). A la premiere ouverture sur une machine neuve, il
REM  n y a donc RIEN pour lancer la Matrice -- sauf ce fichier.
REM
REM  CE QUE FAIT CE FICHIER, DANS L ORDRE :
REM    1. cherche le runtime embarque (runtime\python.exe) ;
REM    2. s il est absent, cherche un python de secours sur la machine, le
REM       lance pour installer le runtime (runtime\installer.py) ;
REM    3. rejoue la verification du runtime installe ;
REM    4. handed over au lanceur, avec l interpreteur embarque.
REM
REM  IL NE FAIT RIEN D AUTRE. Il ne telecharge rien lui-meme, il ne corrige
REM  rien, il n invente aucun remede : le role d installer appartient au runtime
REM  qu il installe -- sinon le meme algorithme devrait exister en double.
REM ==========================================================================
setlocal EnableDelayedExpansion

set "RUNTIME_DIR=%~dp0cerveau-projet\matrix\runtime"
set "RUNTIME_PY=%RUNTIME_DIR%\python.exe"
set "LANCEUR=%~dp0cerveau-projet\matrix\lancer.py"
set "INSTALLER=%RUNTIME_DIR%\installer.py"

REM --- VERIFICATION 1 : le lanceur est-il la ? (une archive mal extraite) -----
if not exist "%LANCEUR%" (
    echo [DEMARRAGE] REFUS : le lanceur est absent : "%LANCEUR%"
    echo [DEMARRAGE] L archive du projet est incomplete ou mal extraite.
    echo [DEMARRAGE] Re-telecharge le depot et extrais-le ENTIEREMENT.
    exit /b 2
)

REM --- VERIFICATION 2 : le runtime embarque est-il deja installe ? -------------
if exist "%RUNTIME_PY%" (
    echo [DEMARRAGE] Runtime embarque present, demarrage direct.
    goto DEMARRER
)

echo [DEMARRAGE] Runtime Python ABSENT ^(%RUNTIME_PY%^)
echo [DEMARRAGE] Le livrable ne contient pas Python : il va etre installe.
echo [DEMARRAGE] Une seule fois -- les suivants demarrages seront directs.

REM --- ETAPE 1/2 : trouver un python de secours --------------------------------
REM  Ordre de recherche nomme et stable : le gestionnaire Python de Microsoft
REM  (alias python3), puis l alias classique, puis le lanceur py.exe.
set "SECOURS="
for %%C in (python3.exe python.exe) do (
    if not defined SECOURS (
        for /f "delims=" %%P in ('where %%C 2^>nul') do (
            if not defined SECOURS set "SECOURS=%%P"
        )
    )
)
if not defined SECOURS (
    for /f "delims=" %%P in ('py -3 -c "import sys;print(sys.executable)" 2^>nul') do (
        if not defined SECOURS set "SECOURS=%%P"
    )
)

if not defined SECOURS (
    echo.
    echo [DEMARRAGE] REFUS : aucun Python trouve sur cette machine.
    echo [DEMARRAGE] Ni le runtime embarque, ni python3, ni python, ni py.exe.
    echo.
    echo [DEMARRAGE] REMEDE, dans cet ordre :
    echo   1. Verifie que Python est installe ^(https://www.python.org/downloads^).
    echo   2. Relance ce fichier. L installation partira toute seule.
    echo.
    echo [DEMARRAGE] Version attendue du runtime : voir runtime\README.md
    exit /b 3
)

echo [DEMARRAGE] Python de secours trouve : %SECOURS%
echo [DEMARRAGE] Installation du runtime embarque en cours...

REM --- ETAPE 2/2 : l installation elle-meme --------------------------------------
REM  C'est le runtime qu on installe qui l'installe : un seul algorithme, dans
REM  un seul langage. Le .cmd ne fait que l'appeler.
"%SECOURS%" "%INSTALLER%"
set "CODE=%errorlevel%"
if not "%CODE%"=="0" (
    echo.
    echo [DEMARRAGE] REFUS : l installation du runtime a echoue ^(code %CODE%^).
    echo [DEMARRAGE] L installation nomme son remede et sa cause juste au-dessus.
    echo [DEMARRAGE] Relance apres avoir lu. Ne contourne pas.
    exit /b 4
)

REM --- ETAPE 3/2 : le runtime est-il vraiment la, maintenant ? -----------------
REM  On ne CROIT pas l installation : on la revérifie par l usage. Un fichier
REM  qui existe n'est pas un interpreteur qui marche (le cas reel du premier
REM  essai : le runtime s'installait mais ne trouvait pas ses modules).
if not exist "%RUNTIME_PY%" (
    echo [DEMARRAGE] REFUS : l installation a rendu 0 mais "%RUNTIME_PY%" est absent.
    exit /b 5
)

"%RUNTIME_PY%" -c "import sys" >nul 2>&1
if errorlevel 1 (
    echo [DEMARRAGE] REFUS : le runtime installe ne s'execute pas ^(code %errorlevel^).
    exit /b 6
)

echo [DEMARRAGE] Runtime installe et verifie.

REM --- ETAPE 4/2 : demarrer, avec l interpreteur embarque ------------------------
:DEMARRER
"%RUNTIME_PY%" "%LANCEUR%" %*
exit /b %errorlevel%