from unittest import TestCase

from webauthn.helpers import parse_attestation_object
from webauthn.helpers.structs import RegistrationCredential
from webauthn.registration.formats.android_safetynet import (
    verify_android_safetynet,
)


class TestVerifyRegistrationResponseAndroidSafetyNet(TestCase):
    def test_verify_attestation_android_safetynet(self) -> None:
        credential = RegistrationCredential.parse_raw(
            """{
            "id": "AePltP2wAoNYwG5XGc9sfleGgDxQRHdkX8vphNIHv3HylIj_nZo9ncs7bLL65AGmVAc69pS4l64hgOBJU9o2jCQ",
            "rawId": "AePltP2wAoNYwG5XGc9sfleGgDxQRHdkX8vphNIHv3HylIj_nZo9ncs7bLL65AGmVAc69pS4l64hgOBJU9o2jCQ",
            "response": {
                "attestationObject": "o2NmbXRxYW5kcm9pZC1zYWZldHluZXRnYXR0U3RtdKJjdmVyaTIxMjYyMTAzN2hyZXNwb25zZVkgXGV5SmhiR2NpT2lKU1V6STFOaUlzSW5nMVl5STZXeUpOU1VsR1dIcERRMEpGWldkQmQwbENRV2RKVVdadE9HbFpXbnAxY1RCRlNrRkJRVUZCU0RkMVVsUkJUa0puYTNGb2EybEhPWGN3UWtGUmMwWkJSRUpIVFZGemQwTlJXVVJXVVZGSFJYZEtWbFY2UldsTlEwRkhRVEZWUlVOb1RWcFNNamwyV2pKNGJFbEdVbmxrV0U0d1NVWk9iR051V25CWk1sWjZTVVY0VFZGNlJWUk5Ra1ZIUVRGVlJVRjRUVXRTTVZKVVNVVk9Ra2xFUmtWT1JFRmxSbmN3ZVUxVVFUTk5WR3Q0VFhwRmVrNUVTbUZHZHpCNVRWUkZkMDFVWTNoTmVrVjZUa1JHWVUxQ01IaEhla0ZhUW1kT1ZrSkJUVlJGYlVZd1pFZFdlbVJETldoaWJWSjVZakpzYTB4dFRuWmlWRU5EUVZOSmQwUlJXVXBMYjFwSmFIWmpUa0ZSUlVKQ1VVRkVaMmRGVUVGRVEwTkJVVzlEWjJkRlFrRkxaazVUUWxsNE0wMDJTbkpKYVRCTVVVUkdORlZhYUhSemVUZ3lRMjgwVG5aM2NpOUdTVzQzTHpsbkszaHpWM3BEV1dkU04xRnpSMjF5ZVVjNWRsQkdja2Q1VVhKRlpHcERVWFZDVTFGVGQyOXZOR2R3YVVocGR6RllibkZHWm5KT1l6SjNURkpQTDFCVWRTdGhhMFpFU1UwMlozVXpaR1JuZDFGWFIwZGFjbFpRZWt0RmFrOTVUbE5HVFVKTU1GZEJTMmwxZFZsQ2RqRTBVWFp1YmxjeFJXdFpZbkZLWkZSb05reFhabVYyWTFkU1N5dFVkRlpoT1hwelIyNUZibWMzYTAxUVYxQkNTekJPTUdKUVozaGlOR3B1ZUdGSWNXeE1lSEV2UTJwRWJreHJSRVZrZFdabFZEVlZaM0pzVkc1M09WVnRXbTFOZUdGUWRHRXZkbm93WTJnMlpteERkM2xwZG1wSGFqSjRWRWhMVmxsMmJWbHdORlJtVEdjd1kxVk9VRVV4WkV0cVRrbGlTMWxEZUZGSlZucHVlSFY0WlhCVVUxWnBXWFZqVUVZMFZuZHVLelpFT1ZwNFVVcEtLeTlsTmt0TVNXdERRWGRGUVVGaFQwTkJia0YzWjJkS2MwMUJORWRCTVZWa1JIZEZRaTkzVVVWQmQwbEdiMFJCVkVKblRsWklVMVZGUkVSQlMwSm5aM0pDWjBWR1FsRmpSRUZVUVUxQ1owNVdTRkpOUWtGbU9FVkJha0ZCVFVJd1IwRXhWV1JFWjFGWFFrSlVUWE5VU1RWeFowRlBVbXRCWkROTlVFd3dOV2cwTm1KdlZsaEVRV1pDWjA1V1NGTk5SVWRFUVZkblFsRnNOR2huVDNOc1pWSnNRM0pzTVVZeVIydEpVR1ZWTjA4MGEycENkRUpuWjNKQ1owVkdRbEZqUWtGUlVtaE5SamgzUzJkWlNVdDNXVUpDVVZWSVRVRkhSMGh0YURCa1NFRTJUSGs1ZGxrelRuZE1ia0p5WVZNMWJtSXlPVzVNTW1Rd1kzcEdhMDVIYkhWa1JFRjRRbWRuY2tKblJVWkNVV04zUVc5WmJHRklVakJqUkc5MlRETkNjbUZUTlc1aU1qbHVURE5LYkdOSE9IWlpNbFo1WkVoTmRsb3pVbnBOVjFFd1RHMVNiR05xUVdSQ1owNVdTRkpGUlVacVFWVm5hRXBvWkVoU2JHTXpVWFZaVnpWclkyMDVjRnBETldwaU1qQjNTVkZaUkZaU01HZENRbTkzUjBSQlNVSm5XbTVuVVhkQ1FXZEZkMFJCV1V0TGQxbENRa0ZJVjJWUlNVWkJla0V2UW1kT1ZraFNPRVZQUkVFeVRVUlRaMDF4UVhkb2FUVnZaRWhTZDA5cE9IWlpNMHB6WTNrMWQyRXlhM1ZhTWpsMlduazVibVJJVFhoYVJGSndZbTVSZGxnd1dsRmpXRVpLVTBka1dVNXFaM1ZaTTBwelRVbEpRa0YzV1V0TGQxbENRa0ZJVjJWUlNVVkJaMU5DT1VGVFFqaFJSSFpCU0ZWQldFNTRSR3QyTjIxeE1GWkZjMVkyWVRGR1ltMUZSR1kzTVdad1NETkxSbnBzVEVwbE5YWmlTRVJ6YjBGQlFVWTJkbmd5VHpGblFVRkNRVTFCVW1wQ1JVRnBRa3AxVjFCU2JWSk5kbXBqVkZWd1NXSnlUa3RvT0hONFlrZDRUbEJOWm14aWNuWXhaSGhVYWtwM1EyZEpaMU01ZDJkTVZVcGxVWEZNVFZJNFdHVnVSMDVtZVZsb1lYRnNjbEo0ZUUwNGMxQTRWa2x3VVVkVFV6QkJaR2RDT1ZCMlREUnFMeXRKVmxkbmEzZHpSRXR1YkV0S1pWTjJSa1J1WjBwbWVUVnhiREpwV21acFRIY3hkMEZCUVZoeEwwaFpLMHRCUVVGRlFYZENTRTFGVlVOSlJESk1NbkpJUW14S2FUbFNSbTlQWmtWQ00yUjRTR1ZJVjFSS2QzTndORFpKWmtscU5tOUxTM0JZWWtGcFJVRXlOVk5aUmswNFp6RlVLMGRKVlhKVlRUQjRZMDVVZDJrdmJISnhhRmxyVVUxSEswWnpNbVp0Um1SSmQwUlJXVXBMYjFwSmFIWmpUa0ZSUlV4Q1VVRkVaMmRGUWtGRU5qaG1lRWhNZUU5REsxWnNUakZTVGtONVMyUlVjV1pJWWxKQlFXUk9XVmczTjBoWEwyMVFRbTVWUXpGb2NtVlVSM2hIZUZOT01VUm9hazF4Tkhwb09GQkRiVEI2TDNKQ00zQkVkMmxuYldsTmRtRllVRVZFYXpaRWJHbE5VMFY1WkRCak5ua3dPV2cxVjA1WFRpOWplR3BITDNWUk1ESjZSRU12UldrdlptUkZaM1V5TVVobmVITTNRMFZVZFROMFpUWkNiekZTZUM5NFIxRnRLMnRvTlhZd2NIWXJhVmw2Y25oVmJFOHZUV1J2YjJsa2VqbENRMWhYT0haeVRVbzJVbk5SVmxKUWVUUjVSbGN2TXpjeU4yeDFSRnBaTUVoME5XMUZSa2xLUTNCV1EybENUSE5wZURCd2JWUnNhMXBhZFhSRWFDOHZUV1JOTlVFME56RldRVU14VTBsNGVrTXpUMkYwZEZoV1RGTnRTWFpuZDFoWFlsbzVhekpzZWtwcGVrRnNiRkpMVld0TlRGUmtjMDlFY0RVek0yNVBhMlJXVTFvMlppdEljbkZKYzFSTVRuTTFVVk5MWWtVMGNuaHlkbFpPS3pROUlpd2lUVWxKUm1wRVEwTkJNMU5uUVhkSlFrRm5TVTVCWjBOUGMyZEplazV0VjB4YVRUTmliWHBCVGtKbmEzRm9hMmxIT1hjd1FrRlJjMFpCUkVKSVRWRnpkME5SV1VSV1VWRkhSWGRLVmxWNlJXbE5RMEZIUVRGVlJVTm9UVnBTTWpsMldqSjRiRWxHVW5sa1dFNHdTVVpPYkdOdVduQlpNbFo2U1VWNFRWRjZSVlZOUWtsSFFURlZSVUY0VFV4U01WSlVTVVpLZG1JelVXZFZha1YzU0doalRrMXFRWGRQUkVWNlRVUkJkMDFFVVhsWGFHTk9UV3BqZDA5VVRYZE5SRUYzVFVSUmVWZHFRa2ROVVhOM1ExRlpSRlpSVVVkRmQwcFdWWHBGYVUxRFFVZEJNVlZGUTJoTldsSXlPWFphTW5oc1NVWlNlV1JZVGpCSlJrNXNZMjVhY0ZreVZucEpSWGhOVVhwRlZFMUNSVWRCTVZWRlFYaE5TMUl4VWxSSlJVNUNTVVJHUlU1RVEwTkJVMGwzUkZGWlNrdHZXa2xvZG1OT1FWRkZRa0pSUVVSblowVlFRVVJEUTBGUmIwTm5aMFZDUVV0MlFYRnhVRU5GTWpkc01IYzVla000WkZSUVNVVTRPV0pCSzNoVWJVUmhSemQ1TjFabVVUUmpLMjFQVjJoc1ZXVmlWVkZ3U3pCNWRqSnlOamM0VWtwRmVFc3dTRmRFYW1WeEsyNU1TVWhPTVVWdE5XbzJja0ZTV21sNGJYbFNVMnBvU1ZJd1MwOVJVRWRDVFZWc1pITmhlblJKU1VvM1R6Qm5Memd5Y1dvdmRrZEViQzh2TTNRMGRGUnhlR2xTYUV4UmJsUk1XRXBrWlVJck1rUm9hMlJWTmtsSlozZzJkMDQzUlRWT1kxVklNMUpqYzJWcVkzRnFPSEExVTJveE9YWkNiVFpwTVVab2NVeEhlVzFvVFVaeWIxZFdWVWRQTTNoMFNVZzVNV1J6WjNrMFpVWkxZMlpMVmt4WFN6TnZNakU1TUZFd1RHMHZVMmxMYlV4aVVrbzFRWFUwZVRGbGRVWktiVEpLVFRsbFFqZzBSbXR4WVROcGRuSllWMVZsVm5SNVpUQkRVV1JMZG5OWk1rWnJZWHAyZUhSNGRuVnpURXA2VEZkWlNHczFOWHBqVWtGaFkwUkJNbE5sUlhSQ1lsRm1SREZ4YzBOQmQwVkJRV0ZQUTBGWVdYZG5aMFo1VFVFMFIwRXhWV1JFZDBWQ0wzZFJSVUYzU1VKb2FrRmtRbWRPVmtoVFZVVkdha0ZWUW1kbmNrSm5SVVpDVVdORVFWRlpTVXQzV1VKQ1VWVklRWGRKZDBWbldVUldVakJVUVZGSUwwSkJaM2RDWjBWQ0wzZEpRa0ZFUVdSQ1owNVdTRkUwUlVablVWVktaVWxaUkhKS1dHdGFVWEUxWkZKa2FIQkRSRE5zVDNwMVNrbDNTSGRaUkZaU01HcENRbWQzUm05QlZUVkxPSEpLYmtWaFN6Qm5ibWhUT1ZOYWFYcDJPRWxyVkdOVU5IZGhRVmxKUzNkWlFrSlJWVWhCVVVWRldFUkNZVTFEV1VkRFEzTkhRVkZWUmtKNlFVSm9hSEJ2WkVoU2QwOXBPSFppTWs1NlkwTTFkMkV5YTNWYU1qbDJXbms1Ym1SSVRubE5WRUYzUW1kbmNrSm5SVVpDVVdOM1FXOVphMkZJVWpCalJHOTJURE5DY21GVE5XNWlNamx1VEROS2JHTkhPSFpaTWxaNVpFaE5kbG96VW5wamFrVjFXa2RXZVUxRVVVZEJNVlZrU0hkUmRFMURjM2RMWVVGdWIwTlhSMGt5YURCa1NFRTJUSGs1YW1OdGQzVmpSM1J3VEcxa2RtSXlZM1phTTFKNlkycEZkbG96VW5wamFrVjFXVE5LYzAxRk1FZEJNVlZrU1VGU1IwMUZVWGREUVZsSFdqUkZUVUZSU1VKTlJHZEhRMmx6UjBGUlVVSXhibXREUWxGTmQwdHFRVzlDWjJkeVFtZEZSa0pSWTBOQlVsbGpZVWhTTUdOSVRUWk1lVGwzWVRKcmRWb3lPWFphZVRsNVdsaENkbU15YkRCaU0wbzFUSHBCVGtKbmEzRm9hMmxIT1hjd1FrRlJjMFpCUVU5RFFXZEZRVWxXVkc5NU1qUnFkMWhWY2pCeVFWQmpPVEkwZG5WVFZtSkxVWFZaZHpOdVRHWnNUR1pNYURWQldWZEZaVlpzTDBSMU1UaFJRVmRWVFdSalNqWnZMM0ZHV21Kb1dHdENTREJRVG1OM09UZDBhR0ZtTWtKbGIwUlpXVGxEYXk5aUsxVkhiSFZvZURBMmVtUTBSVUptTjBnNVVEZzBibTV5ZDNCU0t6UkhRa1JhU3l0WWFETkpNSFJ4U25reWNtZFBjVTVFWm14eU5VbE5VVGhhVkZkQk0zbHNkR0ZyZWxOQ1MxbzJXSEJHTUZCd2NYbERVblp3TDA1RFIzWXlTMWd5VkhWUVEwcDJjMk53TVM5dE1uQldWSFI1UW1wWlVGSlJLMUYxUTFGSFFVcExhblJPTjFJMVJFWnlabFJ4VFZkMldXZFdiSEJEU2tKcmQyeDFOeXMzUzFrelkxUkpabnBGTjJOdFFVeHphMDFMVGt4MVJIb3JVbnBEWTNOWlZITldZVlUzVm5BemVFdzJNRTlaYUhGR2EzVkJUMDk0UkZvMmNFaFBhamtyVDBwdFdXZFFiVTlVTkZnekt6ZE1OVEZtV0VwNVVrZzVTMlpNVWxBMmJsUXpNVVExYm0xelIwRlBaMW95Tmk4NFZEbG9jMEpYTVhWdk9XcDFOV1phVEZwWVZsWlROVWd3U0hsSlFrMUZTM2xIVFVsUWFFWlhjbXgwTDJoR1V6STRUakY2WVV0Sk1GcENSMFF6WjFsblJFeGlhVVJVT1daSFdITjBjR3NyUm0xak5HOXNWbXhYVUhwWVpUZ3hkbVJ2Ulc1R1luSTFUVEkzTWtoa1owcFhieXRYYUZRNVFsbE5NRXBwSzNka1ZtMXVVbVptV0dkc2IwVnZiSFZVVG1OWGVtTTBNV1JHY0dkS2RUaG1Sak5NUnpCbmJESnBZbE5aYVVOcE9XRTJhSFpWTUZSd2NHcEtlVWxYV0doclNsUmpUVXBzVUhKWGVERldlWFJGVlVkeVdESnNNRXBFZDFKcVZ5ODJOVFp5TUV0V1FqQXllRWhTUzNadE1scExTVEF6Vkdkc1RFbHdiVlpEU3pOclFrdHJTMDV3UWs1clJuUTRjbWhoWm1ORFMwOWlPVXA0THpsMGNFNUdiRkZVYkRkQ016bHlTbXhLVjJ0U01UZFJibHB4Vm5CMFJtVlFSazlTYjFwdFJucE5QU0lzSWsxSlNVWlpha05EUWtWeFowRjNTVUpCWjBsUlpEY3dUbUpPY3pJclVuSnhTVkV2UlRoR2FsUkVWRUZPUW1kcmNXaHJhVWM1ZHpCQ1FWRnpSa0ZFUWxoTlVYTjNRMUZaUkZaUlVVZEZkMHBEVWxSRldrMUNZMGRCTVZWRlEyaE5VVkl5ZUhaWmJVWnpWVEpzYm1KcFFuVmthVEY2V1ZSRlVVMUJORWRCTVZWRlEzaE5TRlZ0T1haa1EwSkVVVlJGWWsxQ2EwZEJNVlZGUVhoTlUxSXllSFpaYlVaelZUSnNibUpwUWxOaU1qa3dTVVZPUWsxQ05GaEVWRWwzVFVSWmVFOVVRWGROUkVFd1RXeHZXRVJVU1RSTlJFVjVUMFJCZDAxRVFUQk5iRzkzVW5wRlRFMUJhMGRCTVZWRlFtaE5RMVpXVFhoSmFrRm5RbWRPVmtKQmIxUkhWV1IyWWpKa2MxcFRRbFZqYmxaNlpFTkNWRnBZU2pKaFYwNXNZM2xDVFZSRlRYaEdSRUZUUW1kT1ZrSkJUVlJETUdSVlZYbENVMkl5T1RCSlJrbDRUVWxKUTBscVFVNUNaMnR4YUd0cFJ6bDNNRUpCVVVWR1FVRlBRMEZuT0VGTlNVbERRMmRMUTBGblJVRjBhRVZEYVhnM2FtOVlaV0pQT1hrdmJFUTJNMnhoWkVGUVMwZzVaM1pzT1UxbllVTmpabUl5YWtndk56Wk9kVGhoYVRaWWJEWlBUVk12YTNJNWNrZzFlbTlSWkhObWJrWnNPVGQyZFdaTGFqWmlkMU5wVmpadWNXeExjaXREVFc1NU5sTjRia2RRWWpFMWJDczRRWEJsTmpKcGJUbE5XbUZTZHpGT1JVUlFhbFJ5UlZSdk9HZFpZa1YyY3k5QmJWRXpOVEZyUzFOVmFrSTJSekF3YWpCMVdVOUVVREJuYlVoMU9ERkpPRVV6UTNkdWNVbHBjblUyZWpGcldqRnhLMUJ6UVdWM2JtcEllR2R6U0VFemVUWnRZbGQzV2tSeVdGbG1hVmxoVWxGTk9YTkliV3RzUTJsMFJETTRiVFZoWjBrdmNHSnZVRWRwVlZVck5rUlBiMmR5UmxwWlNuTjFRalpxUXpVeE1YQjZjbkF4V210cU5WcFFZVXMwT1d3NFMwVnFPRU00VVUxQlRGaE1NekpvTjAweFlrdDNXVlZJSzBVMFJYcE9hM1JOWnpaVVR6aFZjRzEyVFhKVmNITjVWWEYwUldvMVkzVklTMXBRWm0xbmFFTk9Oa296UTJsdmFqWlBSMkZMTDBkUU5VRm1iRFF2V0hSalpDOXdNbWd2Y25Nek4wVlBaVnBXV0hSTU1HMDNPVmxDTUdWelYwTnlkVTlETjFoR2VGbHdWbkU1VDNNMmNFWk1TMk4zV25CRVNXeFVhWEo0V2xWVVVVRnpObkY2YTIwd05uQTVPR2MzUWtGbEsyUkVjVFprYzI4ME9UbHBXVWcyVkV0WUx6RlpOMFI2YTNabmRHUnBlbXByV0ZCa2MwUjBVVU4yT1ZWM0szZHdPVlUzUkdKSFMyOW5VR1ZOWVROTlpDdHdkbVY2TjFjek5VVnBSWFZoS3l0MFoza3ZRa0pxUmtaR2VUTnNNMWRHY0U4NVMxZG5lamQ2Y0cwM1FXVkxTblE0VkRFeFpHeGxRMlpsV0d0clZVRkxTVUZtTlhGdlNXSmhjSE5hVjNkd1ltdE9SbWhJWVhneWVFbFFSVVJuWm1jeFlYcFdXVGd3V21OR2RXTjBURGRVYkV4dVRWRXZNR3hWVkdKcFUzY3hia2cyT1UxSE5ucFBNR0k1WmpaQ1VXUm5RVzFFTURaNVN6VTJiVVJqV1VKYVZVTkJkMFZCUVdGUFEwRlVaM2RuWjBVd1RVRTBSMEV4VldSRWQwVkNMM2RSUlVGM1NVSm9ha0ZRUW1kT1ZraFNUVUpCWmpoRlFsUkJSRUZSU0M5TlFqQkhRVEZWWkVSblVWZENRbFJyY25semJXTlNiM0pUUTJWR1RERktiVXhQTDNkcFVrNTRVR3BCWmtKblRsWklVMDFGUjBSQlYyZENVbWRsTWxsaFVsRXlXSGx2YkZGTU16QkZlbFJUYnk4dmVqbFRla0puUW1kbmNrSm5SVVpDVVdOQ1FWRlNWVTFHU1hkS1VWbEpTM2RaUWtKUlZVaE5RVWRIUjFkb01HUklRVFpNZVRsMldUTk9kMHh1UW5KaFV6VnVZakk1Ymt3eVpIcGpha1YzUzFGWlNVdDNXVUpDVVZWSVRVRkxSMGhYYURCa1NFRTJUSGs1ZDJFeWEzVmFNamwyV25rNWJtTXpTWGhNTW1SNlkycEZkVmt6U2pCTlJFbEhRVEZWWkVoM1VYSk5RMnQzU2paQmJHOURUMGRKVjJnd1pFaEJOa3g1T1dwamJYZDFZMGQwY0V4dFpIWmlNbU4yV2pOT2VVMVRPVzVqTTBsNFRHMU9lV0pFUVRkQ1owNVdTRk5CUlU1RVFYbE5RV2RIUW0xbFFrUkJSVU5CVkVGSlFtZGFibWRSZDBKQlowbDNSRkZaVEV0M1dVSkNRVWhYWlZGSlJrRjNTWGRFVVZsTVMzZFpRa0pCU0ZkbFVVbEdRWGROZDBSUldVcExiMXBKYUhaalRrRlJSVXhDVVVGRVoyZEZRa0ZFVTJ0SWNrVnZiemxETUdSb1pXMU5XRzlvTm1SR1UxQnphbUprUWxwQ2FVeG5PVTVTTTNRMVVDdFVORlo0Wm5FM2RuRm1UUzlpTlVFelVta3habmxLYlRsaWRtaGtSMkZLVVROaU1uUTJlVTFCV1U0dmIyeFZZWHB6WVV3cmVYbEZiamxYY0hKTFFWTlBjMmhKUVhKQmIzbGFiQ3QwU21GdmVERXhPR1psYzNOdFdHNHhhRWxXZHpReGIyVlJZVEYyTVhabk5FWjJOelI2VUd3MkwwRm9VM0ozT1ZVMWNFTmFSWFEwVjJrMGQxTjBlalprVkZvdlEweEJUbmc0VEZwb01VbzNVVXBXYWpKbWFFMTBabFJLY2psM05Ib3pNRm95TURsbVQxVXdhVTlOZVN0eFpIVkNiWEIyZGxsMVVqZG9Xa3cyUkhWd2MzcG1ibmN3VTJ0bWRHaHpNVGhrUnpsYVMySTFPVlZvZG0xaFUwZGFVbFppVGxGd2MyY3pRbHBzZG1sa01HeEpTMDh5WkRGNGIzcGpiRTk2WjJwWVVGbHZka3BLU1hWc2RIcHJUWFV6TkhGUllqbFRlaTk1YVd4eVlrTm5hamc5SWwxOS5leUp1YjI1alpTSTZJakp5TlZWak5EQXhieTkxWW5WNWVGbzJUVk4wVGtGa1pXMUlkVGg0UVZReWNXOVFXR2c1WldoeVdUZzlJaXdpZEdsdFpYTjBZVzF3VFhNaU9qRTJNekEzTURNeU5EQXdOVGNzSW1Gd2ExQmhZMnRoWjJWT1lXMWxJam9pWTI5dExtZHZiMmRzWlM1aGJtUnliMmxrTG1kdGN5SXNJbUZ3YTBScFoyVnpkRk5vWVRJMU5pSTZJbXhHVVhkSFYwRklkekZaTkdKNVNsUjRSVWQ0T0hsQmFsVkJlVUZFUW10NFJqTlNaa0pIVHpSMVFUZzlJaXdpWTNSelVISnZabWxzWlUxaGRHTm9JanAwY25WbExDSmhjR3REWlhKMGFXWnBZMkYwWlVScFoyVnpkRk5vWVRJMU5pSTZXeUk0VURGelZ6QkZVRXBqYzJ4M04xVjZVbk5wV0V3Mk5IY3JUelV3UldRclVrSkpRM1JoZVRGbk1qUk5QU0pkTENKaVlYTnBZMGx1ZEdWbmNtbDBlU0k2ZEhKMVpTd2laWFpoYkhWaGRHbHZibFI1Y0dVaU9pSkNRVk5KUXlKOS5NUFlueXVkY3lOQTB1bHM1R0NidXpkTmhvNVhReDkyY2NfUWwyVXdSa1hWdTdPVE5SRVdRTTdHRkN4Wl9TcEJ4ZzBqS1lRd21FX2Z3Rll2U1BqaXlZbmpocENKejFZQjY5bVAwMG9VaHJzTUR2MmgxblQwTjdxd045U2tUTno4WFdnN0VPRDhmcUI0US1NMUNoemdRelNla2RxQXBfSXlrQXdYRjBFM3pqV0xuN2h1WTNjV3FPeFQzNGRSWFBFWkNIMlR1RDRQSUdHcmVJMlkxczlrckY1NjZjZGtfaXRKcGQ3ZlZ4OVVHaEtkNkg3bi02NGtQUzF2VE10WkhkMXRtRExuM3p4aUhTLVJmWFBxT3JEY0NacWcxcXFPdTRnQWpCb1pZbW03RF9oM2gzUVh6aW9ob0ZoeFNpNHVYMjc3NDU1ZHlRSXY2VW02RkpVZWFNOXE4ZEFoYXV0aERhdGFYxUM-aBZp-t3K2T8SiJsc0tHiVg5EKhu4zSaRsspfcKDIRQAAAAC5P9lh8uZGL7EiggAiR954AEEB4-W0_bACg1jAblcZz2x-V4aAPFBEd2Rfy-mE0ge_cfKUiP-dmj2dyztssvrkAaZUBzr2lLiXriGA4ElT2jaMJKUBAgMmIAEhWCCRXy7I5ieefvztqGsBuhKzrZ791MIGmTh9EvllVMBLzyJYIEUi7k0WWjywJtUaxQkA-0zRgEPQCYTP9hkDWi_BTH4j",
                "clientDataJSON": "eyJ0eXBlIjoid2ViYXV0aG4uY3JlYXRlIiwiY2hhbGxlbmdlIjoiczh4cnFMc3hnZXdqdG80c3gzbjFqVFlJUlFCcEhXbjMiLCJvcmlnaW4iOiJodHRwczpcL1wvZGV2aWNlbWFuYWdlbWVudC1kdW8xLnB3bC5uZ3Jvay5pbyIsImFuZHJvaWRQYWNrYWdlTmFtZSI6ImNvbS5hbmRyb2lkLmNocm9tZSJ9"
            },
            "type": "public-key",
            "clientExtensionResults": {}
        }
        """
        )

        parsed_attestation_object = parse_attestation_object(
            credential.response.attestation_object
        )

        # Test the verifier itself so we can activate its timestamp verification bypass
        verified = verify_android_safetynet(
            attestation_statement=parsed_attestation_object.att_stmt,
            attestation_object=credential.response.attestation_object,
            client_data_json=credential.response.client_data_json,
            pem_root_certs_bytes=[],
            verify_timestamp_ms=False,
        )

        assert verified is True
