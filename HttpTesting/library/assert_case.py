
"""
Frame assertion setting.
"""
class Ac:
    """
    Set assertion constant.
    Const:
        eq: Assertion is equal.
        nq: Assert inequality.
        at: Assertion is True.
        af: Assertion is False.
        als: Assert a is b.
        alst: Assert a is not b. 
        an: Assertion is None.
        ann: Assertion is not None.
        ain: Assert a in b.
        nin: Assert a in not b.
        ins: Assert isinstance(a, b).
        nins: Assert not isinstances(a, b).
    """
    eq = "self.assertEquals('{}','{}')"   
    nq = "self.assertNotEqual(str({}),'{}')"
    al = "self.assertIs({}, {})"
    at = "self.assertIsNot({},{})"
    ai = "self.assertIn('{}','{}')"
    ani = "self.assertNotIn('{}','{}')"
    ais = "self.assertlsInstance({},{})"
    anis = "self.assertNotIsInstance({},{})"
    
    ln = "self.assertIsNone({})"
    lnn = "self.assertIsNotNone({})"
    bt = "self.assertTrue({})"
    bf = "self.assertFalse({})"
