import tempfile
import unittest
from pathlib import Path
import tutor_tools as t

class TutorTests(unittest.TestCase):
    def test_retrieval_and_empty(self):
        text='Umsatz ist Erlös.\nGewinn berücksichtigt Kosten.'
        self.assertEqual(t.retrieve(text,'Was bedeutet Umsatz?')[0]['start'],1)
        self.assertEqual(t.retrieve(text,'Liquiditätsplanung'),[])
    def test_quote_validation(self):
        chunks=t.retrieve('Umsatz ist Erlös.','Umsatz')
        answer={'erklaerung':'Umsatz ist Erlös.', 'verstaendnischeck':'Was weißt du?', 'hinweis':'Denke an Erlöse.', 'rueckfrage':'Was könnte es sein?', 'reflexionsaufgabe':'', 'quellenstelle':'Umsatz ist Erlös.', 'quellenstatus':'im_skript'}
        self.assertEqual(t.validate_response(answer,chunks),answer)
        answer['quellenstelle']='Erfundene Quelle'
        with self.assertRaises(ValueError): t.validate_response(answer,chunks)
    def test_progress(self):
        with tempfile.TemporaryDirectory() as d:
            old=t.DB;t.DB=Path(d)/'test.db'
            try:
                t.progress_save('Umsatz','weakness','Üben')
                self.assertEqual(t.progress_list()[0]['status'],'weakness')
                t.progress_save('Umsatz','mastered')
                self.assertEqual(t.progress_list()[0]['status'],'mastered')
                self.assertEqual(t.progress_history()[-1]['mastered'],1)
                t.feedback_save('Umsatz',1)
                t.progress_delete('Umsatz');self.assertEqual(t.progress_list(),[])
                t.project_create('Marketing')
                t.progress_save('Marken','learning','', 'Marketing')
                self.assertEqual(t.progress_list(),[])
                self.assertEqual(t.progress_list('Marketing')[0]['concept'],'Marken')
                self.assertEqual(t.progress_history('Marketing')[-1]['total'],1)
                with self.assertRaises(ValueError): t.progress_save('X','invalid')
            finally:t.DB=old
if __name__=='__main__':unittest.main()
