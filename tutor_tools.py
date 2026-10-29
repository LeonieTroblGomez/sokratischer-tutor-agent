"""Deterministische Skriptsuche, Ausgabeprüfung und lokales Lern-Memory."""
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB = ROOT / 'memory' / 'memory.db'
MIGRATION = ROOT / 'memory' / 'migrations' / '001-initial.sql'

def retrieve(script, question, limit=3):
    """Rangfolge nach gemeinsamen Wörtern; Zeilennummern beziehen sich auf den Originaltext."""
    lines = script.splitlines()
    terms = set(re.findall(r'[\wäöüß]{4,}', question.lower()))
    chunks = []
    for start in range(0, len(lines), 8):
        text = '\n'.join(lines[start:start + 8]).strip()
        if not text:
            continue
        words = set(re.findall(r'[\wäöüß]{4,}', text.lower()))
        chunks.append((len(terms & words), start + 1, min(start + 8, len(lines)), text[:4000]))
    chunks.sort(key=lambda x: (-x[0], x[1]))
    return [{'start': a, 'end': b, 'text': t, 'matches': score} for score, a, b, t in chunks[:limit] if score > 0]

def validate_response(data, chunks):
    expected = {'erklaerung','verstaendnischeck','hinweis','rueckfrage','reflexionsaufgabe','quellenstelle','quellenstatus'}
    if not isinstance(data, dict) or set(data) != expected:
        raise ValueError('Antwort entspricht nicht dem erwarteten Schema.')
    for key in ('verstaendnischeck','hinweis','rueckfrage'):
        if not isinstance(data[key], str) or not data[key].strip() or len(data[key]) > 1000:
            raise ValueError('Ungültiges Antwortfeld: ' + key)
    if not isinstance(data['erklaerung'],str) or not data['erklaerung'].strip() or len(data['erklaerung'])>2000 or not isinstance(data['reflexionsaufgabe'],str) or len(data['reflexionsaufgabe'])>1000:
        raise ValueError('Ungültige Erklärung oder Reflexionsaufgabe.')
    quote = data['quellenstelle']
    if not isinstance(quote, str) or len(quote) > 500 or data['quellenstatus'] not in ('im_skript','nicht_belegt'):
        raise ValueError('Ungültige Quellenangabe.')
    if data['quellenstatus'] == 'im_skript':
        if not quote.strip() or not any(quote in c['text'] for c in chunks):
            raise ValueError('Quellenzitat ist nicht im bereitgestellten Skriptauszug enthalten.')
    elif quote:
        raise ValueError('Unbelegte Antwort darf kein Quellenzitat enthalten.')
    return data

def connect():
    DB.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DB, timeout=5)
    db.executescript(MIGRATION.read_text(encoding='utf-8'))
    return db

def valid_project(project):
    if not isinstance(project,str) or not project.strip() or len(project)>80:
        raise ValueError('Bitte einen Projektnamen bis 80 Zeichen eingeben.')
    return project.strip()

def projects_list():
    with connect() as db:
        return [row[0] for row in db.execute('SELECT name FROM projects ORDER BY name COLLATE NOCASE')]

def project_create(name):
    name=valid_project(name)
    with connect() as db:
        db.execute('INSERT OR IGNORE INTO projects(name) VALUES(?)',(name,))
    return name

def record_progress_history(db, project):
    total, mastered = db.execute("SELECT count(*), count(CASE WHEN status='mastered' THEN 1 END) FROM project_progress WHERE project=?",(project,)).fetchone()
    db.execute('INSERT INTO progress_history(project,total,mastered) VALUES(?,?,?)',(project,total,mastered))

def progress_history(project='Allgemein'):
    project=valid_project(project)
    with connect() as db:
        rows=db.execute('SELECT recorded_at,total,mastered FROM progress_history WHERE project=? ORDER BY id DESC LIMIT 25',(project,)).fetchall()
        return [dict(zip(('recorded_at','total','mastered'), row)) for row in reversed(rows)]

def progress_list(project='Allgemein'):
    project=valid_project(project)
    with connect() as db:
        return [dict(zip(('concept','status','note','updated_at'), row)) for row in db.execute('SELECT concept,status,note,updated_at FROM project_progress WHERE project=? ORDER BY updated_at DESC, concept',(project,))]

def progress_save(concept, status, note='', project='Allgemein'):
    project=valid_project(project)
    concept, note = concept.strip(), note.strip()
    if not concept or len(concept) > 120 or len(note) > 1000 or status not in ('mastered','weakness','learning'):
        raise ValueError('Ungültiger Lernstand.')
    with connect() as db:
        if not db.execute('SELECT 1 FROM projects WHERE name=?',(project,)).fetchone(): raise ValueError('Projekt nicht gefunden.')
        db.execute('INSERT INTO project_progress(project,concept,status,note) VALUES(?,?,?,?) ON CONFLICT(project,concept) DO UPDATE SET status=excluded.status,note=excluded.note,updated_at=CURRENT_TIMESTAMP',(project,concept,status,note))
        record_progress_history(db,project)

def progress_delete(concept, project='Allgemein'):
    project=valid_project(project)
    with connect() as db:
        deleted=db.execute('DELETE FROM project_progress WHERE project=? AND concept=?',(project,concept)).rowcount
        if deleted: record_progress_history(db,project)

def feedback_save(concept, rating, note='', project='Allgemein'):
    project=valid_project(project)
    if not isinstance(concept,str) or not concept.strip() or len(concept)>120 or type(rating) is not int or rating not in (-1,1) or not isinstance(note,str) or len(note)>1000:
        raise ValueError('Ungültiges Feedback.')
    with connect() as db:
        if not db.execute('SELECT 1 FROM projects WHERE name=?',(project,)).fetchone(): raise ValueError('Projekt nicht gefunden.')
        db.execute('INSERT INTO project_feedback(project,concept,rating,note) VALUES(?,?,?,?)',(project,concept.strip(),rating,note.strip()))
