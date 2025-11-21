from django import template
import datetime

from django.contrib.auth.models import GroupManager, Permission
from httplib2.auth import authentication_info

import json

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Permet d'accéder à dict[key] dans les templates."""
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None
"""
                the_description = 'description_'+'{{usedLang}}';
                option.text = element[the_description];
                """


def date_today(value):
    return datetime.date.today()


def getEquivalentLang(value, usedLang):
    if not value.startswith("id_"):
        value = 'id_' + value
    if value in Lang[usedLang]:
        return Lang[usedLang][str(value)]
    else:
        return value


def relatedToLoading(value):
    return value in ['GroupeDivision', 'CompetitionEquipeSaisonGroupe', 'Equipe', 'Terrain', 'JoueurForm']


def filterdata(data, key, default=None):
    #print(data,"  ",key)
    return str(data.get(key, default))


def getElementLength(value):
    return len(value)


def checkContainsNoShow(data, value):
    if '_id' in str(value):
        return True
    is_there = str(value).lower() in data
    return is_there


def checkContainsRender(data, value):
    is_there = str(value).lower() in data
    return is_there


def getTypeInput(data, key, default=None):
    type_ = type(data.get(key, default))
    #print(data," the type ", type_,"  ",'.time' in str(type_))
    if 'str' in str(type_):
        return 'text'
    elif '.date' in str(type_):
        return 'date'
    elif 'date' in str(type_) and 'time' in str(type_):
        return 'datetime'
    elif '.time' in str(type_):
        return 'time'
    elif 'int' in str(type_):
        return 'number'
    elif '.png' in str(type_) or '.pdf' in str(type_):
        return 'file'
    else:
        return 'text'


def isFile(value):
    return value in ['file_PDF', 'pdf', 'PDF', 'photo']


def rolatedToLang(value, usedLang):
    isIn = value in ['nom_ar', 'prenom_ar', 'nom_fr', 'prenom_fr', 'description_ar', 'description_fr', 'intitule',
                     'intitule_arab',
                     'first_name_ar', 'last_name_ar', 'first_name', 'last_name']
    if isIn:

        if str(usedLang) in value:
            return True
        else:
            return False
    else:
        return True


def checkAccess(user, value, appuser=None):
    appuser["username"] = "programmeur"
    #appuser = AppModels.AppUser.objects.get(id=int(user))
    #permissions =  appuser.user_permissions.all()
    #group_permissions = Permission.objects.filter(group__app_users=appuser).distinct()
    #print(group_permissions)
    #print(str(value).lower(),"  ",int(user),"  hh ",appuser.has_perm('forms.view_' + str(value).lower()))
    if appuser.has_perm('forms.view_' + str(value).lower()):
        return True
    else:
        return False

def delgue_or_programmeur(user, appuser=None):
    #print("user",user)
    #appuser = AppModels.AppUser.objects.get(id=int(user))
    appuser["username"]="programmeur"
    #print(appuser.username,"  kk ",appuser.groups)
    if appuser.username=="programmeur":
        return True
    else:
        return False

def checkFormDisplay(btn):
    if str(btn) in ['Arbitre', 'Delegue', 'ResponsableAction', 'Commissionaire']:
        return False
    else:
        return True


def getIconAction(id):
    icons = {
        "1": '/static/img/football.png',
        "3": '/static/img/football.png',
        "5": '/static/img/football.png',
        "6": '/static/img/yellow-card.png',
        "7": '/static/img/red-card.png',

    }
    return icons[str(id)] if str(icons[str(id)]) else ""


def checkTeamConvFull(id):
    return int(id) == 11

def checkTeamConvRempFull(id):
    return int(id) == 9

# app/templatetags/form_extras.py
from django import template
from django.forms.boundfield import BoundField

register = template.Library()


def field_type(field):
    """
    Retourne un identifiant de type pour le widget du champ.
    Exemples possibles:
      - "checkbox"         (CheckboxInput)
      - "clearablefile"    (ClearableFileInput)
      - "file"             (FileInput)
      - "select"           (Select)
      - "radioselect"      (RadioSelect)
      - "textarea"         (Textarea)
      - "date"             (DateInput ou input type="date")
      - "datetime-local"   (DateTimeInput avec type HTML5)
      - "number"           (NumberInput)
      - "email"            (EmailInput)
      - "password"         (PasswordInput)
      - "text"             (TextInput ou par défaut)
    """

    # Accepte soit un BoundField, soit directement un widget
    widget = None
    if isinstance(field, BoundField):
        widget = field.field.widget
    else:
        widget = getattr(field, "widget", None) or getattr(field, "field", None)

    if widget is None:
        return "text"

    # 1) Si le widget a un input_type (HTML5), on s’en sert
    input_type = getattr(widget, "input_type", None)
    if input_type:
        # .input_type peut être "text", "date", "email", "number", etc.
        return str(input_type).lower()

    # 2) Sinon, on renvoie le nom de classe normalisé
    cls_name = widget.__class__.__name__.lower()  # e.g. 'checkboxinput'
    # Petites normalisations utiles
    if "checkbox" in cls_name:
        return "checkbox"
    if "clearablefile" in cls_name:
        return "clearablefile"
    if "fileinput" in cls_name or cls_name == "fileinput":
        return "file"
    if "radioselect" in cls_name:
        return "radioselect"
    if "select" in cls_name:
        return "select"
    if "textarea" in cls_name:
        return "textarea"
    if "date" in cls_name and "datetime" not in cls_name:
        return "date"
    if "datetime" in cls_name:
        return "datetime-local"
    if "number" in cls_name:
        return "number"

    # fallback
    return "text"


register.filter('field_type', field_type)
register.filter('getIconAction', getIconAction)
register.filter('checkFormDisplay', checkFormDisplay)
register.filter('isFile', isFile)
register.filter('checkContainsRender', checkContainsRender)
register.filter('checkContainsNoShow', checkContainsNoShow)
register.filter('filterdata', filterdata)
register.filter('getTypeInput', getTypeInput)
register.filter('relatedToLoading', relatedToLoading)
register.filter('getElementLength', getElementLength)
register.filter('date_today', date_today)
register.filter('getEquivalentLang', getEquivalentLang)
register.filter('get_item', get_item)
register.filter('rolatedToLang', rolatedToLang)
register.filter('checkAccess', checkAccess)
register.filter('isProgrammeur', delgue_or_programmeur)
register.filter('checkTeamConvFull', checkTeamConvFull)
register.filter('checkTeamConvRempFull', checkTeamConvRempFull)

Lang = {
    "ar": {
"id_candidater":"الترشيح",
"id_competitions_section":"المنافسات",
        "id_is_first": "أول تكوين",
        "id_comm_technique": "التكوينات",
        "id_MotifSanctionLois": "قانون سبب العقوبة",
        "id_EquipeSanction": "عقوبة الفريق",
        "id_MotifSanctionEquipe": "أسباب عقوبة الفريق",
        "id_groups": "الصلاحيات",
        "id_slogan": 'العصبة الجهوية كلميم واد نون لكرة القدم',
        "id_login": "تسجيل الدخول",
        "id_logout": "تسجيل الخروج",
        "id_upload_video": "فيدوهات",
        "id_MediaPhotos": "صور",
        "id_matchresult": "نتائج المباريات",
        "id_MatchResult": "نتيجة المباراة",
        "id_home": "الرئيسة",
        "id_ligue": "عصبة كلميم واد نون",
        "id_bureau": "المكتب المديري",
        "id_club": "الأندية",
        "id_archive": "الارشيف",
        "id_assurance ": "التأمين",
        "id_DiplomeArbitrage": "ديبلوم التحكيم",
        "id_allMtch": "مباريات اليوم",
"id_voir_tou":"اظهار الكل",
        "id_validation_result": "تأكيد النتائج",
        "id_mon_equipe": "احصائيات فريقي",
        "id_joueur_stats": "احصائيات اللاعبين",
        "id_nv_saison_param": "موسم كروي جديد",
        "id_suivi_delegue": "تتبع المناديب",
        "id_suivi_delsignation": "تتبع منسقي المناديب",
        "id_homologation_pv": "المصادقة على النتائج",

        "id_commission": "اللجن الجهوية",
        "id_com_lois": "لجنة القوانين و الأنظمة و التأهيل",
        "id_com_esprit": "لجنة التأديب والروح الرياضية",
        "id_com_techn": "اللجنة التقنية",
        "id_com_diversi": "لجنة كرة القدم المتنوعة",
        "id_com_femi": "لجنة كرة القدم النسوية",
        "id_com_progr": "لجنة البرمجة و المسابقات",
        "id_com_appel_regional": "اللجنة الجهوية للإستئناف",
        "id_com_arbitr": "اللجنة الجهوية للتحكيم",

        "id_competition_football": "كرة القدم",
        "id_competition_futsal": "داخل القاعة",
        "id_competition_beach": "الشاطئية",
        "id_competition_women": "النسائية",
        "id_competition_baseball": "القاعدية",
        "id_excelence": "القسم الممتاز",
        "id_honneur1": "القسم الشرفي الأول",
        "id_honneur2": "القسم الشرفي الثاني",
        "id_youngsection": "الفئات الصغرى",

        "id_pvs": "المحاضر",
        "id_ancien_bureau": "المكاتب السابقة",
        "id_regle_loi": " القوانين و الأنظمة",
        "id_reglemen_ligue": "نظام العصبة",
        "id_junior": "الشبان",
        "id_cadet": "الفتيان",
        "id_minimes": "الصغار",
        "id_mmoin_13": "أقل من 13 سنة",
        "id_mmoin_12": "أقل من 12 سنة",
        "id_mmoin_11": "أقل من 11 سنة",
        "id_mmoin_09": "أقل من 9 سنوات",
        "id_activite": "أنشطة العصبة",
        "id_imprime": "مطبوعات",

        "id_approbation": "لجنة الأنظمة والقوانين والمصادقة على النتائج",
        "id_esprit": "اللجنة التأديبية والروح الرياضية",
        "id_appel": "اللجنة الجهوية للإستئناف",

        "id_contact": "اتصل بنا",
        "id_partenaires": "ⵉⵎⴰⴷⵔⴰⵡⵏ  ⵏⵏⵖ - شركاؤنا",
        "id_siege": "مقر العصبة الجهوية كلميم واد نون لكرة القدم",
        "id_siege_next": "شارع .......... كلميم",
        "id_barid": "صندوق البريد ....... كلميم",
        "id_suivre": "تابعنا",

        "id_liens": "روابط مهمة",
        "id_lien_qualif": "نظام تأهيل اللاعبين",
        "id_lien_federation": "الجامعة الملكية المغربية لكرة القدم",
        "id_lien_diver": "العصبة الوطنية لكرة القدم المتنوعة",
        "id_lien_pro": "العصبة الوطنية لكرة القدم الاحترافية",
        "id_lien_amat": "العصبة الوطنية لكرة القدم هواة",
        "id_lien_guide": "دليل المسؤولية المدنية الرياضية",

        "id_voir_tou_news": "اظهار الكل",
        "id_voir_tou_annonces": "اظهار الكل",
        "id_voir_tou_programmes": "اظهار الكل",
        "id_filtres": "بحث",
        "id_matches": "مباريات",
        "id_classements": "الترتيب",
        "id_nouvelle": "آخر الاخبار",
        "id_annonces": "بلاغات",
        "id_program": "البرامج",
        "id_programme": "البرامج",
        "id_rights": "جميع الحقوق محفوظة",
        "id_derni_nouve": "آخر المستجدات",

        "id_ligue_president": "السادة الرؤساء",
        "id_ligue_lumieres": "نجوم كرة القدم الوادنونية",
        "id_valeurs": "قيم العصبة",

        "id_actualites_p": "الاخبار",
        "id_annonces_p": "البلاغات",
        "id_programme_p": "البرامج",

        "id_title": "العنوان",
        "id_thumbnail": "صورة الواجهة",
        "id_firstDescription": "الوصف الاول",
        "id_images": "الصور",
        "id_secondDescription": "الوصف الثاني",
        "id_time": "التاريخ",
        "id_public_news": "أخبار مفتوحة",
        "id_public_annonce": "بلاغات مفتوحة",
        "id_public_slider": "على الواجهة",

        "id_bureau_adm": "المكتب المديري",
        "id_president_status": "الرئيس",
        "id_president_name": "عبد الله ابو القاسم",
        "id_sg_status": "الكاتب العام",
        "id_sg_name": "محمد ابو العباس",

        "id_prenom_fr": "اللقب / Prenom",
        "id_prenom_ar": "اللقب بالعربية",
        "id_license": "رقم الرخصة",
        "id_phone": "الهاتف",
        "id_photo": "Photo Récente (jpg ou png) / صورة حديثة",
        "id_the_player": "اللاعب",
        "id_affecter": "اضافة اللاعبين الى الفريق",
        "id_joueur_non_convoque": "لأئحة اللاعبين",
        "id_joueur_convoque": "اللاعبون المتواجدون على ارضية الملعب",

        "id_joueur_parametre": "إدارة اللاعبين",
        "id_convocation_parametre": "استدعاء اللاعبين",
        "id_manager_matche": "وقائع المباراة",
        "id_delegue_parametre": "مبارياتي",
        "id_delegue_parametre2": "البحث عن مباراة",
        "id_matchtypeaction_parametre": "نوعية أحداث المباراة",
        "id_matchaction_parametre": "أحداث المباراة",

        "id_membre_association_parametre": "أعضاء الجمعية",
        "id_fonction_association_parametre": "الصفة داخل الجمعية",
        "id_mandat_association_parametre": "ولاية الجمعية",
        "id_bureau_association_parametre": "تكوين مكتب الجمعية",

        "id_joueur_entree": "اللاعب البديل",
        "id_joueur_sortie": "اللاعب المستبدل",
        "id_minute_change": "دقية الاستبدال",
        "id_type_action": "نوع الحدث",
        "id_search": "بحث",
        "id_ajouter": "إضافة",
        "id_first_name": "الاسم / Prénom",
        "id_last_name": "اللقب / Nom",
        "id_first_name_ar": "الاسم بالعربية",
        "id_last_name_ar": "اللقب بالعربية",
        "id_delete_btn": "حذف",
        "id_update": "أنتم بصدد إجراء تغييرات",
        "id_update_btn": "تبديل",
        "id_close_btn": "إغلاق",
        "id_email": "البريد الإلكتروني / Email",
        "id_CINorNum": "رقم البطاقة الوطنية أو جواز السفر / N° CIN ou Passeport",
        "id_CIN": "رقم البطاقة الوطنية ",
        "id_date_naissance": "تاريخ الميلاد / Date de naissance",
        "id_username": "اسم المستخدم",
        "id_description_fr": "الوصف بالفرنسية",
        "id_description_ar": "الوصف بالعربية",
        "id_the_first_saison": "موسم أول",
        "id_previous_saison": "الموسم السابق",
        "id_the_pole_sportif": "القطب الرياضي",
        "id_pole_sportif": "القطب الرياضي",
        "id_used_before": "مستعمل",
        "id_region": "الجهة / Région",
        "id_province": "العمالة او الاقليم",
        "id_personne": "الشخص",
        "id_entrainneur": "المدرب",
        "id_diplome_entrainneur": "شهادة التدريب",
        "id_arbitre": "الحكم",
        "id_diplome_arbitre": "شهادة التحكيم",
        "id_type_joueur": "نوعية اللاعب",
        "id_joueurs": "اللاعب",
        "id_the_joueur": "اللاعب",
        "id_goalKeeper": "حارس مرمى",
        "id_saison_sportif": "الموسم الرياضي",
        "id_Licences": "التراخيص",
        "id_nom_fr": "الاسم / Nom",
        "id_nom_ar": "الاسم بالعربية",
        "id_intitule_arab": "الاسم بالعربية",
        "id_number": "رقم الفريق",
        "id_pole_terrain": "القطب الرياضي",
        "id_type_terrain": "نوعية الملعب",
        "id_direction": "المسير",
        "id_creation_date": "تاريخ الإنشاء",
        "id_commune": "الجماعة",
        "id_intitule_equi": "اسم الفريق",
        "id_intitule": "الاسم بالفرنسية",
        "id_abreviation": "الاختصار",
        "id_lieu": "الموقع",
        "id_logo": "الشعار",
        "id_the_pole_categorie": "فئات القطب",
        "id_categorie_pole": "الفئة",
        "id_the_first_dividsion": "هل هو أول قسم",
        "id_previous_dividsion": "القسم السابق",
        "id_the_division": "الأقسام",
        "id_the_saison": "المواسم الرياضية",
        "id_competition": "المنافسات",
        "id_the_equipe": "الفريق",
        "id_equipe": "الفريق",
        "id_the_groupe": "المجموعة",
        "id_competition_equipe_saison_groupe": "تكوين المجموعات",
        "id_equipe_en_repos": "فريق في راحة",
        "id_previous_journee": "الجولة السابقة",
        "id_equipe_Recevante": "الفريق المستقبل",
        "id_equipe_Adverse": "الفريق المنافس",
        "id_journee": "الجولات",
        "id_date": "التاريخ",
        "id_heure": "التوقيت",
        "id_terrain": "الملعب",
        "id_terrainName": "اسم ملعب الاستقبال",
        "id_delegue": "المندوب",
        "id_Vprogramation": "البرمجة",
        "id_joueurs_equipe_recevante": "لاعبو الفريق المستقبل",
        "id_joueurs_equipe_adverse": "لاعبو الفريق المنافس",
        "id_match": "المباراة",
        "id_Staff": "الاطر الرياضية",
        "id_type_arbitre": "نوع الحكم",
        "id_the_type_event": "نوع الحدث",
        "id_the_materiel": "المعدات",
        "id_the_action": "رقم الحدث",
        "id_quantite": "العدد",
        "id_the_pv_type": "نوع المحضر",
        "id_date_Pv": "تاريخ المحضر",
        "id_descriptionPV": "الوصف",
        "id_description": "الوصف",
        "id_file_PDF": "ملف PDF",
        "id_ordresjourpv": "جدول الاعمال",
        "id_commissionspvpresident": "رئيس اللجنة",
        "id_commissionspv": "اعضاء اللجنة",
        "id_motif_sanction": "سبب العقوبة",
        "id_type_sanction": "نوع العقوبة",
        "id_the_pv": "المحضر",
        "id_equipe_chargee": "الفريق المسؤول",
        "id_action": "الحدث",
        "id_AppUser": "المستعمل",
        "id_Commissionaire": "عضو اللجنة",
        "id_CompetitionEquipeSaisonGroupe": "تكوين المجموعات",
        "id_Competition": "المنافسات",
        "id_x": "الاحداثيات X",
        "id_y": "الاحداثيات Y",
        "id_Delegue": "المندوب",
        "id_Entrainneur": "المدرب",
        "id_Equipe": "الفرق",
        "id_EventSessions": "الدورة",
        "id_groupe_division": "المجموعة",
        "id_JoueurEquipe": "لاعب الفريق",
        "id_Journee": "الجولة",
        "id_Programation": "البرمجة",
        "id_Match": "المباراة",
        "id_Materiel": "المعدات",
        "id_MotifSanction": "سبب العقوبة",
        "id_OrdreJourPv": "جدول الاعمال",
        "id_PV": "المحضر",
        "id_Pole": "الأقطاب الرياضية",
        "id_PresidentEquipe": "رئيس الفريق",
        "id_ResponsableAction": "المسؤول",
        "id_saison": "المواسم الرياضية",
        "id_Arbitre": "الحكم",
        "id_Terrain": "الملاعب",
        "id_TypeArbitre": "نوع الحكم",
        "id_TypeEvent": "نوع الحدث",
        "id_TypeJoueur": "نوعية اللاعب",
        "id_TypePV": "نوع المحضر",
        "id_TypeSanction": "نوع العقوبة",
        "id_terrain_acuille": "ملعب الاستقبال",
        "id_pole": "الأقطاب الرياضية",
        "id_pole_categorie": "فئة القطب الرياضي",
        "id_division": "القسم",
        "id_journee_numero": "الدورة",
        "id_equipeRecevante": "الفريق المستقبل",
        "id_equipeAdverse": "الفريق الزائر",
        "id_qualite_terrain": "جودة الملعب",
        "id_password": "كلمة المرور",
        "id_Joueur": "اللاعب",
        "id_GestionMatche": "تدبير المباريات",
        "id_Arbitrage": "توزيع الحكام",
        "id_pole_formation": "قطب التكوين",
        "id_date_deb": "من",
        "id_date_fin": "إلى",
        "id_intervenant": "المتدخلون",
        "id_arbitrage": "تعيين الحكام",
        "id_minute_action": "دقيقة الحدث",

        "id_action_a_faire": "العمليات",
        "id_ajouter_annonce": "اضافة خبر",

        "id_accident_decl": "التصريح بالحادث الرياضي",
        "id_accident_proc": "مسطرة التصريح بالحادث الرياضي",
        "id_accident_metho": "كيفية تعبئة التصريح الخاص بالحادث الرياضي",
        "id_accident_guide": "دليل المسؤولية المدنية الرياضية",
        "id_assurance": "التأمين",

        "id_centre_medical": "المركز الطبي",
        "id_upload_files": "تحميل الملف الطبي",
        "id_verification": "تتبع الملف",
        "id_prise_rdv": "الموعد الطبي",
        "id_infos": "للاتصال بنا",
        "id_localisation": "الموقع",
        "id_photos_videos": "صور و فيديوهات",
        "id_marche_49": "الذكرى 49 للمسيرة الخضراء",

        "id_birthRegion": "جهة الميلاد",
        "id_birthProvince": "إقليم الميلاد",
        "id_birthCommune": "جماعة الميلاد",
        "id_terrainthRegion": "جهة الملعب",
        "id_terrainProvince": "إقليم الملعب",
        "id_communeTerrain": "جماعة الملعب",
        "id_pdf": "ملف PDF",
        "id_Generer_Rapport": "اصدار التقرير",
        "id_archived": " في الأرشيف",
        "id_categorie_pole__pole__description_ar": "القطب الرياضي",
        "id_categorie_pole__pole__description_fr": "القطب الرياضي",
        "id_division__categorie_pole__description_ar": "الفئة",
        "id_division__categorie_pole__pole__description_ar": "القطب الرياضي",
        "id_division__categorie_pole__description_fr": "الفئة",
        "id_division__categorie_pole__pole__description_fr": "القطب الرياضي",
         "id_genre": "الجنس / Sexe",
  "id_nationalite": "الجنسية / Nationalité",
  "id_pays_naissance": "بلد الازدياد / Pays de naissance",
  "id_lieu_naissance": "مكان الازدياد / Lieu de naissance",
  "id_langue": "Langue / اللغة",
  "id_date_issue_CINorPass": "تاريخ إصدار بطاقة التعريف أو جواز السفر / Date d'émission de la CIN ou du Passeport",
  "id_pays_CINorPass": "بلد إصدار بطاقة التعريف أو جواز السفر / Pays de la CIN ou du Passeport",
  "id_date_validite_CINorPass": "تاريخ انتهاء صلاحية بطاقة التعريف أو جواز السفر / Date de validité de la CIN ou du Passeport",
  "id_experience_joueur": "الخبرة كلاعب / Expérience comme joueur",
  "id_experience_entraineur": "الخبرة كمدرب / Expérience comme entraîneur",
  "id_pays": "بلد الإقامة / Pays de résidence",
  "id_cin_pass_verso": "النسخة الخلفية لبطاقة التعريف أو جواز السفر / (pdf) Verso de la CIN ou du Passeport",
  "id_certif_secourisme": "شهادة الإسعافات الأولية / (pdf) Certificat de secourisme",
  "id_certif_medicale": "شهادة طبية / (pdf) Certificat médical",
  "id_fiche_antho_casier": "حسن السيرة أو السجل العدلي / (pdf) Fiche anthropométrique ou casier judiciaire",
  "id_diplome_anticedant": "الديبلوم السابق (في حالة اول تكوين: شهادة فريقكم)  / (Attestation du Club si 1ère Formation) Diplôme antécédant",
   "id_telephone": "رقم الهاتف / Téléphone",
        "id_taille": "القياس / Taille",
        "id_adresse": "العنوان / Adresse" ,
        "id_cin_pass_recto": "النسخة الأمامية والخلفية لبطاقة التعريف أو جواز السفر / (pdf) Recto-Verso CIN ou Passeport",

         "id_liveRegion": "جهة الإقامة",
    "id_liveProvince": "إقليم الإقامة",
    "id_liveCommune": "جماعة الإقامة",
    "id_date_debut_arbitrage": "سنة أول ممارسة",
    "id_pres_type": "رئيس أو مكلف بالفريق",
    "id_arb_type": "مندوب أو حكم",
        "id_submit": "تسجيل",
        "id_next": "التالي / Suivant",
        "id_previous": "السابق / Précédent",
        "id_formation": "تكوين",
        "id_form": "استمارة الترشح",
        "id_session_formation": "دورة التكوين",
        "id_please_complete_fields": "المرجو تعبئة / Merci de remplir les champs",
        "id_code": "الرمز / Code",
        "id_intitule_fr": "العنوان بالفرنسية",
        "id_intitule_ar": "العنوان بالعربية",
        "id_duree_heures": "عدد الساعات",
        "id_capacite_par_defaut": "عدد المقاعد",
        "id_actif": "مفعل/غير مفعل",
        "id_session": "الدورات",
        "id_formations": "التكوينات",
        "id_we_will_contact_you": "شكرا على اهتمامكم، ستتم مراسلتكم بعد معالجة ملفكم",
        "id_success": "تم التسجيل بنجاح",
        "id_error": "خطأ أثناء التسجيل",
        "id_Enre_candidat": "تعبئة استمارة الترشح",
        "id_gestion_candid": "إدارة المترشحين",
        "id_prerequis": "المتطلبات القبلية",
        "id_certification": "مدة الامتحان",
        "id_stage_au_club": "عدد ساعات التدريب في النادي",
        "id_mise_en_situation": "مدة التكوين",
        "id_en_salle": "في القاعة",
        "id_objectif": "الاهداف",
        "id_trios": "ثلاثيات التحكيم",
        "id_frais_deplacement": "مصاريف التنقل",
        "id_frais_arbitrage": "مصاريف التحكيم",
        "id_Categorie_Arbitre": "أصناف الحكام",
        "id_Affectation_categorie": "تصنيف الحكام",
        "id_categorie_arbitrage": "صنف الحكم",
        "id_frais_rapport": "تتبع المصاريف",
        "id_check_invalid_input": "بعض الخانات فارغة!!",
        "id_check_invalid_email": "المرجو مراجعة بريدكم الالكتروني",
"id_rib": "رقم الحساب البنكي (24 رقم)",
"id_rib_bancaire": "وثيقة رقم الحساب البنك",
"id_alert_files": "إذا كنتم أضفتم صورا  ملفات من OneDrive أو Google Drive فالمرجو تحميلها على هاتفكم أو حاسوبكم أولا قبل اضافتها هنا",

        "id_FIRST_NEWS": "انطلاق الموسم الجديد",
        "id_second_news": "مواهب فئة أقل من 19 سنة بجهة كلميم واد نون في الواجهة",
        "id_third_news": "إعطاء انطلاقة البطولة الجهوية لكرة القدم داخل القاعة"

    },
    "fr": {
        "id_FIRST_NEWS": "Lancement de la nouvelle saison régionale",
        "id_second_news": "Les talents U19 de Guelmim-Oued Noun à l’honneur",
        "id_third_news": " Coup d’envoi du championnat régional de Futsal",
"id_check_invalid_input": "Des Champs sont vides!!",
"id_frais_rapport": "Rapport Frais",
"id_check_invalid_email": "Merci de vérifier l'Email Saisi",
"id_rib": "Le numéro du compte Bancaire (24 Chiffres) Facultatif",
"id_rib_bancaire": "RIB Bancaire",
"id_categorie_arbitrage": "Catégotrie Arbitre",
"id_alert_files": "Si vous joigner des fichiers depuis <strong>OneDrive</strong> ou <strong>Google Drive</strong>, Merci de les enregistrer sur votre Téléphone ou Ordinateur d'abord, puis de les sélectionner ici.",
"id_ancien_bureau": "Anciens Bureaux",
        "id_regle_loi": " Règlements et Lois",
        "id_reglemen_ligue": "Règlement de la Ligue",
        "id_junior": "Juniors",
        "id_cadet": "Cadets",
        "id_minimes": "Minimes",
        "id_mmoin_13": "Moins de 13 ans",
        "id_mmoin_12": "Moins de 12 ans",
        "id_mmoin_11": "Moins de 11 ans",
        "id_mmoin_09": "Moins de 9 ans",
        "id_youngsection": "Catégories Jeunes",
        "id_activite": "Activités",
        "id_imprime": "Imprimés",
"id_candidater":"Candidature",
"id_prerequis": "Prérequis",
        "id_certification": "Durée de l'examen",
        "id_stage_au_club": "Nombre d'heures de stage en club",
        "id_mise_en_situation": "Durée de la formation",
        "id_en_salle": "En salle",
        "id_objectif": "الاهداف",
"id_voir_tou":"Voir Tout",
"id_allMtch":"Matches du jour",
"id_competition_women":"Féminine",
"id_competition_baseball":"GRASSROOT",
"id_comm_technique":"FORMATIONS",
"id_is_first": "Première formation",
"id_competitions_section":"COMPÉTITIONS",
"id_gestion_candid": "Gestion des candidats",
        "id_session": "Sessions",
        "id_formations": "Formations",
        "id_we_will_contact_you": "ٍMerci pour votre intérêt, Vous serez contacté prochainement",
        "id_success": "Enregistré avec succès",
        "id_error": "Erreur lors de l'enregistrement",
        "id_Enre_candidat": "Remplir le formulaire",
        "id_code": "code",
        "id_intitule_fr": "Intitule Francais",
        "id_intitule_ar": "Intitule Arabe",
        "id_duree_heures": "Duree Heures",
        "id_capacite_par_defaut": "Nombre de places",
        "id_actif": "Active / Désactivée",
        "id_archived":"Archivé",
        "id_joueurs": "Joueur",
        "id_division__categorie_pole__description_ar": "Categorie",
        "id_division__categorie_pole__pole__description_ar": "Pole Sportif",
        "id_division__categorie_pole__description_fr": "Categorie",
        "id_division__categorie_pole__pole__description_fr": "Pole Sportif",
        "id_categorie_pole__pole__description_fr": "Pole Sportif",
        "id_categorie_pole__pole__description_ar": "Pole Sportif",
        "id_photos_videos": "Photos & Videos",
        "id_marche_49": "49ème Anniversaire de la Marche Verte",
        "id_EquipeSanction": "Sanction Equipe",
        "id_MotifSanctionEquipe": "Mofif Sanction Equipe",
        "id_MotifSanctionLois": "Lois Mofif Sanction",
        "id_groups": "Access",
        'id_slogan': 'Ligue Régionale Guelmim Oued Noun de Football',
        "id_login": "Se Connecter",
        "id_logout": "Se déconnecter",
        "id_Staff": "Cadres Sportifs",
        "id_upload_video": "Videos",
        "id_MediaPhotos": "Photos",
        "id_MatchResult": "Résultat du match",
        "id_Generer_Rapport": "Générer Rapport",
        "id_home": "Accueil",
        "id_ligue": "Ligue Guelmim Oued Noun",
        "id_bureau": "Bureau",
        "id_club": "Club",
        "id_archive": "Archives",
        "id_assurance": "Assurance",
        "id_description": "description",



        "id_trios": "Trios D'Arbitrage",
        "id_frais_deplacement": "Frais Deplacement",
        "id_frais_arbitrage": "Frais Arbitrage",
        "id_Categorie_Arbitre": "Categorie Arbitre",
        "id_Affectation_categorie": "Affectation Arbitre au categorie",

        "id_accident_decl": "Formulaire de Déclaration",
        "id_accident_proc": "Procedures pour Déclarer",
        "id_accident_metho": "Comment Remplir la déclaration",
        "id_accident_guide": "Guide de la responsabilité civile sportive",

        "id_minute_action": "Temps Operation",
        "id_commission": "Commissions",
        "id_com_lois": "Commission des Lois, Règlements et Qualifications",
        "id_com_techn": "Comité Technique",
        "id_com_diversi": "Commission du Football Diversifié",
        "id_com_femi": "Commission du Football Féminin",
        "id_com_progr": "Comité de programmation et des compétitions",
        "id_com_appel_regional": "Comité d'Appel Régional",
        "id_com_arbitr": "Comité Régional d'Arbitrage",
        "id_com_esprit": "Commission de Discipline et d'Esprit Sportif",
        "id_DiplomeArbitrage": "Diplome d'Arbitrage",
        "id_competition_football": "Foot-Ball",
        "id_competition_futsal": "Futsal",
        "id_competition_beach": "Soccer Beach",
        "id_excelence": "Excellence",
        "id_honneur1": "Honneur I",
        "id_honneur2": "Honneur II",

        "id_pvs": "PVs",
        "id_approbation": "Approbation des Résultats",
        "id_esprit": "Descipline et Esprit Sportif",
        "id_appel": "Comité d'Appel",
        "id_validation_result": "Validation des Résultats",
        "id_homologation_pv": "Homologation des Résultats",

        "id_contact": "Contact",
        "id_partenaires": "Nos partenaires",
        "id_siege": "Siège de la Ligue Régionale Guelmim Oued Noun de Football ",
        "id_siege_next": "Rue ---- Guelmim",
        "id_suivre": "Suivez-nous",


        "id_action_a_faire": "Opérations",
        "id_actualites_p": "Actualités",
        "id_annonces_p": "Annonces",
        "id_programme_p": "Programme",
        "id_programme": "Programmes",

        "id_title": "Titre",
        "id_thumbnail": "Image de Face",
        "id_firstDescription": "Première Description",
        "id_images": "Images",
        "id_secondDescription": "Deuxième Description",
        "id_time": "Date",
        "id_public_news": "Annonce Ouverte",
        "id_public_slider": "Slider",
        "id_ajouter_annonce": "Ajouter une Actualité",

        "id_liens": "Liens Utiles",
        "id_lien_qualif": "Qualification des Joueurs",
        "id_lien_federation": "Fédération Royale Marocaine du Football",
        "id_lien_diver": "Ligue Nationale de Football Diversifié",
        "id_lien_pro": "Ligue Nationale de Football Professionelle",
        "id_lien_amat": "Ligue National de Football Amateur",
        "id_lien_guide": "Guide de la Responsabilite Civile Sportive",

        "id_voir_tou_news": "Toutes Les Actualités",
        "id_voir_tou_annonces": "Toutes Les Annonces",
        "id_voir_tou_programmes": "Tout Les Programmes",
        "id_filtres": "Filtres",
        "id_matches": "Matches",
        "id_classements": "Classement",
        "id_nouvelle": "Nouveau",
        "id_annonces": "Annonces",
        "id_program": "Programmes",
        "id_rights": "Tous Droits Réservés",
        "id_derni_nouve": "Dernières Nouvelles",

        "id_ligue_president": "Mrs. les Présidents",
        "id_ligue_lumieres": "Etoiles de Guelmim Oued Noun",
        "id_valeurs": "Valeurs de la Ligue",
        "id_infos": "Pour Nous Contacter",
        "id_localisation": "LOCALISATION",

        "id_bureau_adm": "Bureau Administratif",
        "id_president_status": "Président",
        "id_president_name": "Abdellah Abou El Kacem",
        "id_sg_status": "Secrétaire Général",
        "id_sg_name": "Mohammed Abou El Abbas",

        "id_prenom_fr": "Prenom en Français",
        "id_prenom_ar": "Prenom en Arabe",
        "id_license": "Licence",
        "id_phone": "Téléphone",
        "id_photo": "Photo",
        "id_affecter": "Affecter",
        "id_joueur_non_convoque": "---sdfsdfsdf",
        "id_joueur_convoque": "*****sdfsdfsdf",

        "id_joueur_parametre": "Joueur",
        "id_convocation_parametre": "Convactions",
        "id_manager_matche": "Actions Matche",
        "id_delegue_parametre": "Mes Matches",
        "id_delegue_parametre2": "Recherche Matche",
        "id_matchtypeaction_parametre": "Type Action du Matche",
        "id_matchaction_parametre": "Actions du Matche",

        "id_membre_association_parametre": "Membre Association",
        "id_fonction_association_parametre": "Fonction Association",
        "id_mandat_association_parametre": "Mandat Association",
        "id_bureau_association_parametre": "Bureau Association",

        "id_type_action": "Type Action",

        "id_search": "Rechercher",
        "id_arbitrage": "Désignation des Arbitres",
        "id_ajouter": "Ajouter",
        "id_first_name": "Nom en Français",
        "id_last_name": "Prenom en Arabe",
        "id_first_name_ar": "Nom en Français",
        "id_last_name_ar": "Prenom en Arabe",
        "id_delete_btn": "Supprimer",
        "id_update_btn": "Mise à jour",
        "id_update": "Vous êtes entrain de modifier!!",
        "id_close_btn": "Fermer",
        "id_email": "Email",
        "id_CIN": "CIN",
        "id_CINorNum": "CIN ou Passeport",
        "id_date_naissance": "Date de Naissance",
        "id_username": "Login",
        "id_the_first_saison": "Première Saison",
        "id_previous_saison": "Saison Précédente",
        "id_the_pole_sportif": "Pôle Sportif",
        "id_pole_sportif": "Pôle Sportif",
        "id_used_before": "Utilisé Précedemment",
        "id_region": "Région",
        "id_province": "Province",
        "id_personne": "Personne",
        "id_entrainneur": "Entraîneur",
        "id_diplome_entrainneur": "Diplôme d'Entraînnement",
        "id_arbitre": "Arbitre",
        "id_diplome_arbitre": "Diplôme d'Arbitrage",
        "id_type_joueur": "Type Joueur",
        "id_the_joueur": "Joueur",
        "id_saison_sportif": "Saison Sportive",
        "id_Licences": "Licences",
        "id_nom_fr": "Nom en Français",
        "id_nom_ar": "Nom en Arabe",
        "id_intitule_arab": "Nom en Arabe",
        "id_number": "Numéro",
        "id_pole_terrain": "Pôle Terrain",
        "id_pole_formation": "Pôle Formation",
        "id_date_deb": "Date Début",
        "id_date_fin": "Date Fin",
        "id_intervenant": "Intervenants",
        "id_qualite_terrain": "Qualité du Terrain",
        "id_type_terrain": "Type Terrain",
        "id_direction": "Sous la Direction",
        "id_creation_date": "Date de Création",
        "id_commune": "Commune",
        "id_intitule_equi": "Nom Equipe",
        "id_intitule": "Nom en Français",
        "id_abreviation": "Abréviation",
        "id_lieu": "Lieu",
        "id_logo": "Logo",
        "id_pdf": "Fichier PDF",
        "id_pole_categorie": "Sous Pôle",
        "id_categorie_pole": "Sous Pôle",
        "id_the_first_dividsion": "Est-elle la première Division",
        "id_previous_dividsion": "Division Précédente",
        "id_the_division": "Division",
        "id_the_saison": "Saison Sportive",
        "id_competition": "Compétitions",
        "id_the_equipe": "Équipe",
        "id_equipe": "Équipe",
        "id_the_groupe": "Groupe",
        "id_competition_equipe_saison_groupe": "Composition des Groupes",
        "id_equipe_en_repos": "Équipe en Repos",
        "id_previous_journee": "Journée Précédente",
        "id_equipe_Recevante": "Équipe Recevante",
        "id_equipe_Adverse": "Équipe Adverse",
        "id_journee": "Journée",
        "id_date": "Date",
        "id_heure": "Heure",
        "id_terrain": "Terrain",
        "id_terrainName": "Terrain D'accueil",
        "id_delegue": "Délégué",
        "id_Vprogramation": "Programmation",
        "id_joueurs_equipe_recevante": "Joueurs de l'Équipe Recevante",
        "id_joueurs_equipe_adverse": "Joueurs de l'Équipe Adverse",
        "id_match": "Match",
        "id_type_arbitre": "Type Arbitre",
        "id_description_fr": "Description en Français",
        "id_description_ar": "Description en Arabe",
        "id_the_type_event": "Type Évènement",
        "id_the_materiel": "Matériel",
        "id_the_action": "Actions",
        "id_quantite": "Quantité",
        "id_the_pv_type": "Type PV",
        "id_date_Pv": "Date PV",
        "id_descriptionPV": "Description PV",
        "id_file_PDF": "Fichier PDF",
        "id_ordresjourpv": "Ordres du Jour",
        "id_x": "Position X",
        "id_y": "Position Y",
        "id_commissionspvpresident": "Président de Commission",
        "id_commissionspv": "Commissions PV",
        "id_motif_sanction": "Motif Sanction",
        "id_type_sanction": "Type Sanction",
        "id_the_pv": "PV",
        "id_equipe_chargee": "Équipe Chargée",
        "id_action": "Actions",
        "id_AppUser": "Utilisateurs",
        "id_Commissionaire": "Commissaires",
        "id_CompetitionEquipeSaisonGroupe": "Composition des Groupes",
        "id_Competition": "Compétition",
        "id_Delegue": "Délégué",
        "id_Entrainneur": "Entraîneur",
        "id_Equipe": "Équipe",
        "id_EventSessions": "Sessions",
        "id_groupe_division": "Groupe",
        "id_JoueurEquipe": "Joueur d'Equipe",
        "id_Journee": "Journée",
        "id_Programation": "Programation",
        "id_Match": "Match",
        "id_Materiel": "Matériel",
        "id_MotifSanction": "Motif Sanction",
        "id_OrdreJourPv": "Ordre du Jour",
        "id_PV": "PV",
        "id_Pole": "Pôles Sportif",
        "id_PresidentEquipe": "Président Equipe",
        "id_ResponsableAction": "Responsable Action",
        "id_saison": "Saisons Sportives",
        "id_Arbitre": "Arbitre",
        "id_Terrain": "Terrains",
        "id_TypeArbitre": "Type Arbitre",
        "id_TypeEvent": "Type Evénement",
        "id_TypeJoueur": "Type joueur",
        "id_TypePV": "Type PV",
        "id_TypeSanction": "Type sanction",
        "id_terrain_acuille": "Terrain d'Accueil",
        "id_pole": "Pôle Sportif",

        "id_division": "Division",
        "id_journee_numero": "N° Journée",
        "id_equipeRecevante": "Equipe Recevante",
        "id_equipeAdverse": "Equipe Adverse",
        "id_password": "Mot de Passe",
        "id_Joueur": "Joueur",
        "id_GestionMatche": "Gestion Matches",
        "id_Arbitrage": "Affectation Arbitres",

        "id_centre_medical": "Centre Médical",
        "id_upload_files": "Chargement du dossier",
        "id_verification": "Etat Dossier",
        "id_prise_rdv": "Rendez-Vou Médical",

        "id_mon_equipe": "Stats Mon Equipe",
        "id_joueur_stats": "Stats des Joueurs",
        "id_nv_saison_param": "Configuration Nouvelle Saison",
        "id_suivi_delegue": "Suivi Delegues",
        "id_suivi_delsignation": "Suivi Coordinateurs",

         "id_birthRegion": "region de naissance",
        "id_birthProvince": "province de naissance",
        "id_birthCommune": "commune de naissance",
        "id_terrainthRegion": "region de stadium",
        "id_terrainProvince": "province de stadium",
        "id_communeTerrain": "commune de stadium",

        "id_liveRegion": "région de résidence",
    "id_liveProvince": "province de résidence",
    "id_liveCommune": "commune de résidence",
    "id_genre": "Genre",
  "id_nationalite": "Nationalité",
  "id_pays_naissance": "Pays de naissance",
  "id_lieu_naissance": "Lieu de naissance",
  "id_arabe": "Niveau Arabe",
  "id_francais": "Niveau Français",
  "id_anglais": "Niveau Anglais",
  "id_date_issue_CINorPass": "Date de délivrance CIN ou Passeport",
  "id_pays_CINorPass": "Pays de délivrance CIN ou Passeport",
  "id_date_validite_CINorPass": "Date d’expiration CIN ou Passeport",
  "id_experience_joueur": "Experience en tant que Joueur",
  "id_pays": "Pays de résidence",
  "id_cin_pass_verso": "Verso CIN ou Passeport",
  "id_certif_secourisme": "Certificat de secourisme",
  "id_certif_medicale": "Certificat médical",
  "id_fiche_antho_casier": "Casier judiciaire ou attestation de bonne conduite",
  "id_diplome_anticedant": "Diplôme précédent (Attestation du Club pour Formation D)",
"id_telephone": "Numéro de téléphone",
  "id_taille": "Taille",
  "id_adresse": "Adresse",
  "id_cin_pass_recto": "Recto CIN ou Passeport",
"id_experience_entraineur": "Experience en tant qu'Enraineur",
        "id_submit": "Enregistrer",
        "id_next": "Suivant",
        "id_previous": "Précédent",
        "id_formation": "Formation",
        "id_form": "Formulaire De Candidature",
        "id_please_complete_fields": "SVP, Completer les champs"

    },
    "am": {
        'id_slogan': 'العصبة الجهوية كلميم واد نون لكرة القدم',

        "id_search": "Recherch",
        "id_ajouter": "ⴰⵣⵓⵍ",
        "id_first_name": "ⵙⴰⵏ ⵏⵉⵎⴳⴰ",
        "id_last_name": "ⵙⴰⵏ ⴰⵙⴻⵏⵙ",
        "id_delete_btn": "ⵍⵢⴰⵏⴰ",
        "id_update_btn": "ⵜⴰⵔⵓⵏⵜ",
        "id_email": "ⵉⵎⴰⵍ",
        "id_CIN": "ⵙⴷⴰⵍ ⴰⵎⴰⵣⴳⴳⴰⵙ",
        "id_date_naissance": "ⴰⵙⴳⴳⴰⴷ ⴰⴳⵍⴰⵔ",
        "id_username": "ⵙⵉⵏⵏⴰⴷⴰⵙ",
        "id_the_first_saison": "ⵜⴰⵏⴽⴰⵙⵜ ⴰⵙⵉⵙⵡⴰ",
        "id_previous_saison": "ⵜⴰⵏⴽⴰⵙⵜ ⴰⴽⴳⴳⴰ",
        "id_the_pole_sportif": "ⵜⴰⵎⴰⵢⴰⴹⴰⵏ ⴰⵙⴰⵡⵉⴷ",
        "id_pole_sportif": "ⵜⴰⵎⴰⵢⴰⴹⴰⵏ ⴰⵙⴰⵡⵉⴷ",
        "id_used_before": "ⴰⵎⴳⴳⴰⵎ ⴰⴽⴰⵍ",
        "id_region": "ⴰⵏⴰⵎ",
        "id_province": "ⵜⴰⴳⴳⵯⵉ",
        "id_personne": "ⴰⴳⵏⴰⵡ",
        "id_entrainneur": "ⵎⴷⵔⴰⵍⴰⵏ",
        "id_diplome_entrainneur": "ⴰⴷⴼⵍⵓⵎ ⵎⴷⵔⴰⵍⴰⵏ",
        "id_arbitre": "ⴰⵔⴱⵉⵜⵉ",
        "id_diplome_arbitre": "ⴰⴷⴼⵍⵓⵎ ⵎⵉⵙⴳⴰⴱⵉ",
        "id_type_joueur": "ⵓⵢⴰⵍ ⴷⵓⵙⵙⵉⵏ",
        "id_the_joueur": "ⵓⵢⴰⵍ",
        "id_saison_sportif": "ⵜⴰⵏⴽⴰⵙⵜ ⴰⵙⴰⵡⵉⴷ",
        "id_Licences": "ⵍⵉⵙⴰⴷⴰ",
        "id_nom": "ⵓⵔⵜ",
        "id_pole_terrain": "ⵜⴰⴳⴳⴰⵎⵜ ⴰⵜⵔⴰⵢ",
        "id_type_terrain": "ⵓⵙⴰⵢ ⵜⴰⵜⵔⴰⵢ",
        "id_direction": "ⴷⴰⵔⵙⴰ",
        "id_creation_date": "ⵜⴰⵎⴰⵣⵉⵖⵜ ⵏ ⵊⵉⵎⵉⵔ",
        "id_commune": "ⵎⴰⴳⵎⵓⵏ",
        "id_intitule_equi": "ttttttttt",
        "id_intitule": "ⵜⴰⴷⵡⴰⵢⵜ",
        "id_abreviation": "ⵍⴽⵓⵍⵓⵎ",
        "id_lieu": "ⵎⵓⵏⴰ",
        "id_logo": "ⵍⵓⴳⵓ",
        "id_the_pole_categorie": "ⵜⴰⴳⴳⴰⵎⵜ ⴰⵜⴰⵙⵉⴷⴰ",
        "id_the_first_dividsion": "ⵜⴰⵏⴽⴰⵙⵜ ⴰⵙⴰⵎⵎⴰⵙⵉⴷⵓ",
        "id_previous_dividsion": "ⵜⴰⵏⴽⴰⵙⵜ ⴰⴽⴳⴳⴰⵏⵉ",
        "id_the_division": "ⵜⴰⵏⴽⴰⵙⵜ",
        "id_the_saison": "ⵜⴰⵏⴽⴰⵙⵜ",
        "id_competition": "ⵜⴰⵡⵉⴱⵉ",
        "id_the_equipe": "ⵜⴰⴳⴳⴰⵎⵜ",
        "id_the_groupe": "ⵜⴰⴷⴳⵍⴰ",
        "id_competition_equipe_saison_groupe": "ⵜⴰⵡⵉⴱⵉ ⵜⴰⴳⴳⴰⵎⵜ ⵜⴰⵏⴽⴰⵙⵜ ⵜⴰⴷⴳⵍⴰ",
        "id_equipe_en_repos": "ⵜⴰⴳⴳⴰⵎⵜ ⵉⵏ ⴰⵙⵏⵙⵉ",
        "id_previous_journee": "ⵜⴰⵏⵙⵉⵎⴰⵢⵜ ⴰⴽⴳⴳⴰ",
        "id_equipe_Recevante": "ⵜⴰⴳⴳⴰⵎⵜ ⴰⵙⵊⴰⴱⴰⵏⵜ",
        "id_equipe_Adverse": "ⵜⴰⴳⴳⴰⵎⵜ ⴰⴰⴽⵓⴳⵎⴰⵏ",
        "id_journee": "ⵜⴰⵏⵙⵉⵎⴰⵢⵜ",
        "id_Programation": "Programation",
        "id_date": "ⴰⴳⵔⴰ",
        "id_heure": "ⵜⴰⵙⵙⴰⵡⵉⵏ",
        "id_terrain": "ⵜⵉⵔⴰⵢ",
        "id_terrainName": "ⵜⵉⵔⴰⵢ",
        "id_delegue": "ⴷⴻⵍⴻⴳ",
        "id_Vprogramation": "ⵜⵉⵎⴰⵣⵉⵖⵜ",
        "id_joueurs_equipe_recevante": "ⵎⴰⵊⵓⵔ ⴰⵙⴻⴷⴷⴰⵔⴰ ⴰⵙⵊⴰⴱⴰⵏⵜ",
        "id_joueurs_equipe_adverse": "ⵎⴰⵊⵓⵔ ⴰⵙⴻⴷⴷⴰⵔⴰ ⴰⴰⴽⵓⴳⵎⴰⵏ",
        "id_match": "ⵜⴰⵎⵏⴰ",
        "id_type_arbitre": "ⵜⵉⵢⴰⵔⵜ ⴰⵔⴱⵉⵜ",
        "id_description": "ⵉⵙⵏⴰⵡ",
        "id_the_type_event": "ⵜⵓⵙⵉⴷⴰ ⴰⵔⴱⵉⵜ",
        "id_the_materiel": "ⵜⴰⵏⵎⵉⵔⵉⵍⵉ",
        "id_the_action": "ⵜⴰⵔⵓⵏⵜ",
        "id_quantite": "ⵜⵓⵔⵓⴽⵉⵜ",
        "id_the_pv_type": "ⵜⵓⴽⵉⵜ ⴰⴽⵓⵏⵜ",
        "id_date_Pv": "ⴰⴳⵔⴰ ⴰⴽⵓⵏⵜ",
        "id_descriptionPV": "ⵉⵙⵏⴰⵡ ⴰⴽⵓⵏⵜ",
        "id_file_PDF": "ⴰⴽⵔⴰⴱ PDF",
        "id_ordresjourpv": "ⴰⵙⵙⵓⴳ ⴰⵖⴰⵔⵙ ⴰⴽⵓⵏⵜ",
        "id_commissionspvpresident": "ⴰⴽⵓⵙ ⴰⴳⵔⵉⵍⵓ ⴰⴽⵓⵏⵜ",
        "id_commissionspv": "ⴰⴽⵓⵙ ⴰⴽⵓⵏⵜ",
        "id_motif_sanction": "ⵜⴰⵜⵉⵡⴰ ⵉⵎⴳⴰⵔⴰ",
        "id_type_sanction": "ⵜⵓⵢⴰⵔⵜ ⵉⵎⴳⴰⵔⴰ",
        "id_the_pv": "ⵜⵓⴽⵉⵜ",
        "id_equipe_chargee": "ⵜⴰⴳⴳⴰⵎⵜ ⴰⴽⵔⴰⵍ",
        "id_action": "ⴰⴽⵓⵙ",
        "id_AppUser": "Utilisateurs",
        "id__polecategorie": "Sous Pôle Sportif",
        "id_Commissionaire": "Commissaire",
        "id_CompetitionEquipeSaisonGroupe": "Compétition Équipe Saison Groupe",
        "id_Competition": "Compétition",
        "id_Delegue": "Délégué",
        "id_division": "Division",
        "id_Entrainneur": "Entraîneur",
        "id_Equipe": "Équipes",
        "id_EventSessions": "Sessions Évènement",
        "id_groupe_division": "Groupe",
        "id_JoueurEquipe": "Joueur d'Equipe",
        "id_Journee": "Journée",
        "id_Match": "Match",
        "id_Materiel": "Matériel",
        "id_MotifSanction": "Motif de Sanction",
        "id_OrdreJourPv": "Ordre du Jour",
        "id_PV": "PV",
        "id_Pole": "Pôle Sportif",
        "id_PresidentEquipe": "Président de l'équipe",
        "id_ResponsableAction": "Responsable de l'action",
        "id_saison": "Saison Sportive",
        "id_Arbitre": "Arbitre",
        "id_Terrain": "Terrains",
        "id_TypeArbitre": "Type d'arbitre",
        "id_TypeEvent": "Type Évènement",
        "id_TypeJoueur": "Type de joueur",
        "id_TypePV": "Type de PV",
        "id_TypeSanction": "Type de sanction",
        "id_terrain_acuille": "Terrain d'Accueil",
        "id_pole": "Pôle Sportif",
        "id_pole_categorie": "Sous Pôle Sportif",
        "id_journee_numero": "N° Journée",
        "id_equipeRecevante": "Equipe Recevante",
        "id_equipeAdverse": "Equipe Adverse",
        "id_password": "Mot de Passe",
        "id_Joueur": "Joueur",
        "id_GestionMatche": "Gestion Matches",
        "id_Arbitrage": "Affectation Arbitres",

         "id_birthRegion": "region de naissance",
        "id_birthProvince": "province de naissance",
        "id_birthCommune": "commune de naissance",
        "id_terrainthRegion": "region de stadium",
        "id_terrainProvince": "province de stadium",
        "id_communeTerrain": "commune de stadium",

        "id_liveRegion": "région de résidence",
    "id_liveProvince": "province de résidence",
    "id_liveCommune": "commune de résidence",
        "id_submit": "Enregistrer",
        "id_next": "Suivant",
        "id_previous": "Précédent",
        "id_formation": "Formation",
        "id_form": "Formulaire De Candidature",
        "id_please_complete_fields": "SVP, Completer les champs",


    },
    "en": {
          "id_MotifSanctionLois": "Law sanction reason",
  "id_EquipeSanction": "Team sanction",
  "id_MotifSanctionEquipe": "Reasons for team sanction",
  "id_groups": "Permissions",
  "id_slogan": "Regional League Guelmim Oued Noun Football",
  "id_login": "Login",
  "id_logout": "Logout",
  "id_upload_video": "Videos",
  "id_MediaPhotos": "Photos",
  "id_matchresult": "Match results",
  "id_MatchResult": "Match result",
  "id_home": "Home",
  "id_ligue": "Guelmim Oued Noun League",
  "id_bureau": "Executive board",
  "id_club": "Clubs",
  "id_archive": "Archive",
  "id_assurance ": "Sports insurance",
  "id_DiplomeArbitrage": "Refereeing diploma",
  "id_allMtch": "Today's matches",
  "id_validation_result": "Validate results",
  "id_mon_equipe": "My team statistics",
  "id_joueur_stats": "Player statistics",
  "id_nv_saison_param": "New football season",
  "id_suivi_delegue": "Delegate monitoring",
  "id_suivi_delsignation": "Coordinator monitoring",
  "id_homologation_pv": "Results approval",
  "ID_FIRST_NEWS": "Lancement de la nouvelle saison régionale",
  "id_second_news": "Les talents U19 de Guelmim-Oued Noun à l’honneur",
  "id_third_news": " Coup d’envoi du championnat régional de Futsal",
  "id_forth_news": "Results approval",
  "id_fifth_news": "Results approval",

  "id_commission": "Regional committees",
  "id_com_lois": "Laws, regulations & qualification committee",
  "id_com_esprit": "Disciplinary & fair play committee",
  "id_com_techn": "Technical committee",
  "id_com_diversi": "Diverse football committee",
  "id_com_femi": "Women's football committee",
  "id_com_progr": "Programming & competitions committee",
  "id_com_appel_regional": "Regional appeal committee",
  "id_com_arbitr": "Regional refereeing committee",

  "id_competition_football": "Football",
  "id_competition_futsal": "Futsal",
  "id_competition_beach": "Beach soccer",
  "id_competition_women": "Women's football",
  "id_competition_baseball": "Grassroots",
  "id_excelence": "Premier division",
  "id_honneur1": "First honorary division",
  "id_honneur2": "Second honorary division",
  "id_youngsection": "Youth categories",


  "id_approbation": "Regulations & results approval committee",
  "id_esprit": "Disciplinary & fair play committee",
  "id_appel": "Regional appeal committee",

  "id_contact": "Contact us",
  "id_partenaires": "Our partners",
  "id_siege": "Headquarters of the Guelmim Oued Noun regional league",
  "id_siege_next": "Larache Street, Al Mohammadi, 80000 Agadir",
  "id_barid": "P.O. Box 134 Agadir",
  "id_suivre": "Follow us",

  "id_liens": "Important links",
  "id_lien_qualif": "Player qualification system",
  "id_lien_federation": "Royal Moroccan Football Federation",
  "id_lien_diver": "National amateur football league",
  "id_lien_pro": "National professional football league",
  "id_lien_amat": "National amateur football league",
  "id_lien_guide": "Sports civil liability guide",

  "id_voir_tou_news": "Show all",
  "id_voir_tou_annonces": "Show all",
  "id_voir_tou_programmes": "Show all",
  "id_filtres": "Search",
  "id_matches": "Matches",
  "id_classements": "Standings",
  "id_nouvelle": "Latest news",
  "id_annonces": "Announcements",
  "id_program": "Programs",
  "id_programme": "Programs",
  "id_rights": "All rights reserved",
  "id_derni_nouve": "Latest updates",

  "id_ligue_president": "Presidents",
  "id_ligue_lumieres": "Oued Noun football stars",
  "id_valeurs": "League values",

  "id_actualites_p": "News",
  "id_annonces_p": "Announcements",
  "id_programme_p": "Programs",

  "id_title": "Title",
  "id_thumbnail": "Thumbnail",
  "id_firstDescription": "First description",
  "id_images": "Images",
  "id_secondDescription": "Second description",
  "id_time": "Date",
  "id_public_news": "Public news",
  "id_public_annonce": "Public announcements",
  "id_public_slider": "On homepage",

  "id_bureau_adm": "Executive board",
  "id_president_status": "President",
  "id_president_name": "Abdellah Abou El Qassem",
  "id_sg_status": "General secretary",
  "id_sg_name": "Mohamed Abou El Abbas",

  "id_prenom_fr": "Last name (French)",
  "id_prenom_ar": "Last name (Arabic)",
  "id_license": "License number",
  "id_phone": "Phone",
  "id_photo": "Profile photo",
  "id_the_player": "Player",
  "id_affecter": "Add players to team",
  "id_joueur_non_convoque": "Player list",
  "id_joueur_convoque": "Players on the field",

  "id_joueur_parametre": "Player management",
  "id_convocation_parametre": "Player convocations",
  "id_manager_matche": "Match details",
  "id_delegue_parametre": "My matches",
  "id_delegue_parametre2": "Search for match",
  "id_matchtypeaction_parametre": "Match event type",
  "id_matchaction_parametre": "Match events",

  "id_membre_association_parametre": "Association members",
  "id_fonction_association_parametre": "Association role",
  "id_mandat_association_parametre": "Association mandate",
  "id_bureau_association_parametre": "Association executive board",

  "id_joueur_entree": "Substitute player",
  "id_joueur_sortie": "Replaced player",
  "id_minute_change": "Substitution minute",
  "id_type_action": "Event type",
  "id_search": "Search",
  "id_ajouter": "Add",
  "id_first_name": "First name (French)",
  "id_last_name": "Last name (French)",
  "id_first_name_ar": "First name (Arabic)",
  "id_last_name_ar": "Last name (Arabic)",
  "id_delete_btn": "Delete",
  "id_update": "You are about to make changes",
  "id_update_btn": "Update",
  "id_close_btn": "Close",
  "id_email": "Email",
  "id_CINorNum": "National ID or Passport number",
  "id_CIN": "National ID or Passport number",
  "id_date_naissance": "Date of birth",
  "id_username": "Username",
  "id_description_fr": "Description (French)",
  "id_description_ar": "Description (Arabic)",
  "id_the_first_saison": "First season",
  "id_previous_saison": "Previous season",
  "id_the_pole_sportif": "Sports division",
  "id_pole_sportif": "Sports division",
  "id_used_before": "Used",
  "id_region": "Region",
  "id_province": "Province",
  "id_personne": "Person",
  "id_entrainneur": "Coach",
  "id_diplome_entrainneur": "Coaching certificate",
  "id_arbitre": "Referee",
  "id_diplome_arbitre": "Refereeing certificate",
  "id_type_joueur": "Player type",
  "id_joueurs": "Player",
  "id_the_joueur": "Player",
  "id_goalKeeper": "Goalkeeper",
  "id_saison_sportif": "Sports season",
  "id_Licences": "Licenses",
  "id_nom_fr": "Name (French)",
  "id_nom_ar": "Name (Arabic)",
  "id_intitule_arab": "Name (Arabic)",
  "id_number": "Team number",
  "id_pole_terrain": "Sports division",
  "id_type_terrain": "Field type",
  "id_direction": "Manager",
  "id_creation_date": "Creation date",
  "id_commune": "Commune",
  "id_intitule_equi": "Team name",
  "id_intitule": "Name (French)",
  "id_abreviation": "Abbreviation",
  "id_lieu": "Location",
  "id_logo": "Logo",
  "id_the_pole_categorie": "Division category",
  "id_categorie_pole": "Category",
  "id_the_first_dividsion": "Is it the first division?",
  "id_previous_dividsion": "Previous division",
  "id_the_division": "Division",
  "id_the_saison": "Sports season",
  "id_competition": "Competition",
  "id_the_equipe": "Team",
  "id_equipe": "Team",
  "id_the_groupe": "Group",
  "id_competition_equipe_saison_groupe": "Group formation",
  "id_equipe_en_repos": "Resting team",
  "id_previous_journee": "Previous round",
  "id_equipe_Recevante": "Home team",
  "id_equipe_Adverse": "Away team",
  "id_journee": "Round",
  "id_date": "Date",
  "id_heure": "Time",
  "id_terrain": "Field",
  "id_terrainName": "Home field name",
  "id_delegue": "Delegate",
  "id_Vprogramation": "Scheduling",
  "id_joueurs_equipe_recevante": "Home team players",
  "id_joueurs_equipe_adverse": "Away team players",
  "id_match": "Match",
  "id_Staff": "Sports staff",
  "id_type_arbitre": "Referee type",
  "id_the_type_event": "Event type",
  "id_the_materiel": "Equipment",
  "id_the_action": "Event number",
  "id_quantite": "Quantity",

  "id_descriptionPV": "Description",
  "id_description": "Description",
  "id_file_PDF": "PDF file",
  "id_ordresjourpv": "Agenda",
  "id_commissionspvpresident": "Committee president",
  "id_commissionspv": "Committee members",
  "id_motif_sanction": "Sanction reason",
  "id_type_sanction": "Sanction type",

  "id_equipe_chargee": "Responsible team",
  "id_action": "Event",
  "id_AppUser": "User",
  "id_Commissionaire": "Committee member",
  "id_CompetitionEquipeSaisonGroupe": "Group formation",
  "id_Competition": "Competitions",
  "id_x": "X coordinates",
  "id_y": "Y coordinates",
  "id_Delegue": "Delegate",
  "id_Entrainneur": "Coach",
  "id_Equipe": "Teams",
  "id_EventSessions": "Session",
  "id_groupe_division": "Group",
  "id_JoueurEquipe": "Team player",
  "id_Journee": "Round",
  "id_Programation": "Scheduling",
  "id_Match": "Match",
  "id_Materiel": "Equipment",
  "id_MotifSanction": "Sanction reason",
  "id_OrdreJourPv": "Agenda",

  "id_Pole": "Sports divisions",
  "id_PresidentEquipe": "Team president",
  "id_ResponsableAction": "Responsible",
  "id_saison": "Sports seasons",
  "id_Arbitre": "Referee",
  "id_Terrain": "Fields",
  "id_TypeArbitre": "Referee type",
  "id_TypeEvent": "Event type",
  "id_TypeJoueur": "Player type",

  "id_TypeSanction": "Sanction type",
  "id_terrain_acuille": "Home field",
  "id_pole": "Sports divisions",
  "id_pole_categorie": "Division category",
  "id_division": "Division",
  "id_journee_numero": "Round",
  "id_equipeRecevante": "Home team",
  "id_equipeAdverse": "Away team",
  "id_qualite_terrain": "Field quality",
  "id_password": "Password",
  "id_Joueur": "Player",
  "id_GestionMatche": "Match management",
  "id_Arbitrage": "Referee assignments",
  "id_pole_formation": "Training division",
  "id_date_deb": "From",
  "id_date_fin": "To",
  "id_intervenant": "Participants",
  "id_arbitrage": "Referee assignments",
  "id_minute_action": "Event minute",

  "id_action_a_faire": "Actions",
  "id_ajouter_annonce": "Add announcement",

  "id_accident_decl": "Sports accident declaration",
  "id_accident_proc": "Sports accident procedure",
  "id_accident_metho": "How to fill the sports accident declaration",
  "id_accident_guide": "Sports civil liability guide",
  "id_assurance": "Sports insurance",

  "id_centre_medical": "Medical center",
  "id_upload_files": "Upload medical file",
  "id_verification": "Track file",
  "id_prise_rdv": "Medical appointment",
  "id_infos": "Contact us",
  "id_localisation": "Location",
  "id_photos_videos": "Photos & videos",
  "id_marche_49": "49th anniversary of the Green March",

  "id_birthRegion": "Birth region",
  "id_birthProvince": "Birth province",
  "id_birthCommune": "Birth commune",
  "id_terrainthRegion": "Field region",
  "id_terrainProvince": "Field province",
  "id_communeTerrain": "Field commune",
  "id_pdf": "PDF file",
  "id_Generer_Rapport": "Generate report",
  "id_archived": "Archived",
  "id_categorie_pole__pole__description_ar": "Sports division",
  "id_categorie_pole__pole__description_fr": "Sports division",
  "id_division__categorie_pole__description_ar": "Category",
  "id_division__categorie_pole__pole__description_ar": "Sports division",
  "id_division__categorie_pole__description_fr": "Category",
  "id_division__categorie_pole__pole__description_fr": "Sports division",
"id_pv_match": "Match report",
  "id_pv_reunion": "Meeting report",
  "id_pv_arbitre": "Referee report",
  "id_pv_discipline": "Disciplinary report",
  "id_genre": "Gender",
  "id_nationalite": "Nationality",
  "id_pays_naissance": "Country of birth",
  "id_lieu_naissance": "Place of birth",
  "id_arabe": "Arabic level",
  "id_francais": "French level",
  "id_anglais": "English level",
  "id_date_issue_CINorPass": "ID card or passport issue date",
  "id_pays_CINorPass": "ID card or passport issuing country",
  "id_date_validite_CINorPass": "ID card or passport expiry date",
  "id_experience_joueur": "Playing experience",
  "id_experience_entraineur": "Coaching experience",
  "id_pays": "Country of residence",
  "id_cin_pass_verso": "Back side of ID card or passport",
  "id_certif_secourisme": "First aid certificate",
  "id_certif_medicale": "Medical certificate",
  "id_fiche_antho_casier": "Criminal record or good conduct",
  "id_diplome_anticedant": "Previous diploma",
  "id_telephone": "Phone number",
  "id_taille": "Height",
  "id_adresse": "Address",
  "id_cin_pass_recto": "Front side of ID card or passport",

  "id_liveRegion": "Residence region",
  "id_liveProvince": "Residence province",
  "id_liveCommune": "Residence commune",
  "id_date_debut_arbitrage": "First refereeing year",
  "id_pres_type": "Team president or responsible",
  "id_arb_type": "Delegate or referee",
        "id_submit":"Save",
        "id_next":"Next",
        "id_previous":"Previous",
        "id_formation":"Formation",
        "id_form":"Form application",
        "id_please_complete_fields":"Please complete fields",
    }
}
