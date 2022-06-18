import os
import sys
import unittest

from asn1crypto import csr, util

from ._unittest_compat import patch

patch()

byte_cls = bytes
num_cls = int

tests_root = os.path.dirname(__file__)
fixtures_dir = os.path.join(tests_root, "fixtures")


class CSRTests(unittest.TestCase):
    def test_parse_csr(self):
        with open(os.path.join(fixtures_dir, "test-inter-der.csr"), "rb") as f:
            certification_request = csr.CertificationRequest.load(f.read())

        cri = certification_request["certification_request_info"]

        self.assertEqual("v1", cri["version"].native)

        self.assertEqual(
            util.OrderedDict(
                [
                    ("country_name", "US"),
                    ("state_or_province_name", "Massachusetts"),
                    ("locality_name", "Newbury"),
                    ("organization_name", "Codex Non Sufficit LC"),
                    ("organizational_unit_name", "Testing Intermediate"),
                    ("common_name", "Will Bond"),
                    ("email_address", "will@codexns.io"),
                ]
            ),
            cri["subject"].native,
        )
        self.assertEqual(
            util.OrderedDict(
                [
                    ("algorithm", "rsa"),
                    ("parameters", None),
                ]
            ),
            cri["subject_pk_info"]["algorithm"].native,
        )
        self.assertEqual(
            24141757533938720807477509823483015516687050697622322097001928034085434547050399731881871694642845241206788286795830006142635608141713689209738431462004600429798152826994774062467402648660593454536565119527837471261495586474194846971065722669734666949739228862107500673350843489920495869942508240779131331715037662761414997889327943217889802893638175792326783316531272170879284118280173511200768884738639370318760377047837471530387161553030663446359575963736475504659902898072137674205021477968813148345198711103071746476009234601299344030395455052526948041544669303473529511160643491569274897838845918784633403435929,  # noqa
            cri["subject_pk_info"]["public_key"].parsed["modulus"].native,
        )
        self.assertEqual(65537, cri["subject_pk_info"]["public_key"].parsed["public_exponent"].native)
        self.assertEqual([], cri["attributes"].native)

    def test_parse_csr2(self):
        with open(os.path.join(fixtures_dir, "test-third-der.csr"), "rb") as f:
            certification_request = csr.CertificationRequest.load(f.read())

        cri = certification_request["certification_request_info"]

        self.assertEqual("v1", cri["version"].native)

        self.assertEqual(
            util.OrderedDict(
                [
                    ("country_name", "US"),
                    ("state_or_province_name", "Massachusetts"),
                    ("locality_name", "Newbury"),
                    ("organization_name", "Codex Non Sufficit LC"),
                    ("organizational_unit_name", "Test Third-Level Certificate"),
                    ("common_name", "Will Bond"),
                    ("email_address", "will@codexns.io"),
                ]
            ),
            cri["subject"].native,
        )
        self.assertEqual(
            util.OrderedDict(
                [
                    ("algorithm", "rsa"),
                    ("parameters", None),
                ]
            ),
            cri["subject_pk_info"]["algorithm"].native,
        )
        self.assertEqual(
            24242772097421005542208203320016703216069397492249392798445262959177221203301502279838173203064357049006693856302147277901773700963054800321566171864477088538775137040886151390015408166478059887940234405152693144166884492162723776487601158833605063151869850475289834250129252480954724818505034734280077580919995584375189497366089269712298471489896645221362055822887892887126082288043106492130176555423739906252380437817155678204772878611148787130925042126257401487070141904017757131876614711613405231164930930771261221451019736883391322299033324412671768599041417705072563016759224152503535867541947310239343903761461,  # noqa
            cri["subject_pk_info"]["public_key"].parsed["modulus"].native,
        )
        self.assertEqual(65537, cri["subject_pk_info"]["public_key"].parsed["public_exponent"].native)
        self.assertEqual(
            [
                util.OrderedDict(
                    [
                        ("type", "extension_request"),
                        (
                            "values",
                            [
                                [
                                    util.OrderedDict(
                                        [
                                            ("extn_id", "basic_constraints"),
                                            ("critical", False),
                                            (
                                                "extn_value",
                                                util.OrderedDict(
                                                    [
                                                        ("ca", False),
                                                        ("path_len_constraint", None),
                                                    ]
                                                ),
                                            ),
                                        ]
                                    ),
                                    util.OrderedDict(
                                        [
                                            ("extn_id", "key_usage"),
                                            ("critical", False),
                                            (
                                                "extn_value",
                                                {"digital_signature", "non_repudiation", "key_encipherment"},
                                            ),
                                        ]
                                    ),
                                ]
                            ],
                        ),
                    ]
                ),
            ],
            cri["attributes"].native,
        )

    def test_parse_csr3(self):
        with open(os.path.join(fixtures_dir, "test-windows-host.csr"), "rb") as f:
            certification_request = csr.CertificationRequest.load(f.read())

        cri = certification_request["certification_request_info"]

        self.assertEqual("v1", cri["version"].native)

        self.assertEqual(
            util.OrderedDict(
                [
                    ("common_name", "windows.host.example.net"),
                ]
            ),
            cri["subject"].native,
        )
        self.assertEqual(
            util.OrderedDict(
                [
                    ("algorithm", "rsa"),
                    ("parameters", None),
                ]
            ),
            cri["subject_pk_info"]["algorithm"].native,
        )
        self.assertEqual(
            0x00BD5B280774E2E64A2C022ABD50DE7817AAEC50367E94B9C6459CA876DAAF3BC3D7FFC41BF902422AC9AF7D369EEB23245C5D8E2DDA5434463F1D3E596C066A3CBE936BD89B4B7B9923FF6E654608CD3AA1FBC36543165752DDE12C889C7AEE4B5423E311E507BFD9FA60166290AE766005209120B651C3CDECEABBA90B115341D656CB1FE94F372BA7C170BD15261685E92303205A7E5141928415F748D77EE4C6ECF8749B80C07D99F99F9AFF629BE62840E43E4696D6602DF2A7A5E1BF11925021F2DF2F4D27EF42E4DECB0DC615C29EECACA628721A0C3C70C2700B7C658D6B7B7B6285593FD7D5AE086447BDC30429C7231DB6B831D44E4C019887542F5F,  # noqa
            cri["subject_pk_info"]["public_key"].parsed["modulus"].native,
        )
        self.assertEqual(65537, cri["subject_pk_info"]["public_key"].parsed["public_exponent"].native)
        self.assertEqual(
            [
                util.OrderedDict(
                    [
                        ("type", "microsoft_os_version"),
                        ("values", ["6.2.9200.2"]),
                    ]
                ),
                util.OrderedDict(
                    [
                        ("type", "microsoft_request_client_info"),
                        (
                            "values",
                            [
                                util.OrderedDict(
                                    [
                                        ("clientid", 5),
                                        ("machinename", "windows.host.example.net"),
                                        ("username", "locuser"),
                                        ("processname", "MMC.EXE"),
                                    ]
                                )
                            ],
                        ),
                    ]
                ),
                util.OrderedDict(
                    [
                        ("type", "microsoft_enrollment_csp_provider"),
                        (
                            "values",
                            [
                                util.OrderedDict(
                                    [
                                        ("keyspec", 1),
                                        ("cspname", "Microsoft RSA SChannel Cryptographic Provider"),
                                        ("signature", ()),
                                    ]
                                )
                            ],
                        ),
                    ]
                ),
                util.OrderedDict(
                    [
                        ("type", "extension_request"),
                        (
                            "values",
                            [
                                [
                                    util.OrderedDict(
                                        [
                                            ("extn_id", "microsoft_enroll_certtype"),
                                            ("critical", False),
                                            (
                                                "extn_value",
                                                "Machine",
                                            ),
                                        ]
                                    ),
                                    util.OrderedDict(
                                        [
                                            ("extn_id", "extended_key_usage"),
                                            ("critical", False),
                                            (
                                                "extn_value",
                                                ["client_auth", "server_auth"],
                                            ),
                                        ]
                                    ),
                                    util.OrderedDict(
                                        [
                                            ("extn_id", "key_usage"),
                                            ("critical", False),
                                            (
                                                "extn_value",
                                                {"digital_signature", "key_encipherment"},
                                            ),
                                        ]
                                    ),
                                    util.OrderedDict(
                                        [
                                            ("extn_id", "key_identifier"),
                                            ("critical", False),
                                            (
                                                "extn_value",
                                                bytearray.fromhex(
                                                    "2a 98 4b c1 ff 6e 16 ed 2d 69 35 0a 26 e7 1f 8c 05 4f b8 e6"
                                                ),  # noqa
                                            ),
                                        ]
                                    ),
                                ]
                            ],
                        ),
                    ]
                ),
            ],
            cri["attributes"].native,
        )
