from django.test import TestCase
from recommand.models import recommand

class recommandTestCase(TestCase):
    def setUp(self):
        recommand.objects.create(id=1, idBook_id="12345", status="abuse")
        recommand.objects.create(id=2, idBook_id="123456", status="abuse")
        recommand.objects.create(id=3, idBook_id="123457", status="s")
        recommand.objects.create(id=4, idBook_id="123458", status="allowed")

    def test_getValueByStatus(self):
        res,statusNumber,mes = recommand.getValueByStatus("allowed", "idBook_id")
        self.assertEqual(mes , "123458")

    def test_get(self):
        obj = recommand.objects.all().filter(status="abuse")
        print obj[0]
        print obj[1]
        self.assertEqual(obj[1].idBook_id , "123456")
