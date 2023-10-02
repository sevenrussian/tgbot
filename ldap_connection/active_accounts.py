import ldap
from config import bot_login, bot_password


async def get_active_accounts(base, filter) -> list:
    """
    :param base:
    :param filter:
    :return: []

    Возвращает список пользователей из LDAP по указанным контейнерам и фильтрам
    """
    try:
        bot = ldap.initialize('ldap://1.1.1.1:389')
        bot.protocol_version = ldap.VERSION3
        bot.set_option(ldap.OPT_REFERRALS, 0)
        bot.simple_bind_s(bot_login, bot_password)
        scope = ldap.SCOPE_SUBTREE
        attrs = ['name', 'mail', 'proxyAddresses']
        result_set = []
        all_accounts = []
        ldap_result_id = bot.search_ext(base, scope, filter, attrs)

        try:
            while 1:
                result_type, result_data = bot.result(ldap_result_id, 0)
                if (result_data == []):
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        result_set.append(result_data)
        except ldap.SIZELIMIT_EXCEEDED:
            print("Error")

        for user in result_set:
            name = user[0][1].get('name')
            proxyAddresses = user[0][1].get('proxyAddresses')
            mail = user[0][1].get('mail')
            if (proxyAddresses):
                for email_b in proxyAddresses:
                    email = email_b.decode("utf-8")
                    all_accounts.append(email.split(':')[1])
            else:
                all_accounts.append([name[0].decode("utf-8"), mail[0].decode("utf-8")])

        return all_accounts

    except ldap.SERVER_DOWN:
        print("LDAP error: connection error")
        return []
    except ldap.INVALID_CREDENTIALS:
        print("LDAP error: password or login incorrect")
        return []


async def get_all_active_accounts() -> list:
    """
    :return: []

    Возвращает список всех активных аккаунтов и контактов из LDAP

    [[name, email], ...]
    """
    # Options for accounts from Active folder in AD
    base_accounts = "OU=Active,DC=company,DC=ru"
    filter_accounts = "(&(objectCategory=person)(objectClass=user)(!(userAccountControl=2))(mail=*))"

    # Options for contacts from Contacts folder in AD
    base_contacts = "OU=Contacts,DC=company,DC=ru"
    filter_contacts = "(&(objectCategory=person)(objectClass=contact)(mail=*))"

    return await get_active_accounts(base_accounts, filter_accounts) + await get_active_accounts(base_contacts, filter_contacts)


async def is_user_email_active(user_email) -> bool:
    """
    :param user_email: str
    :return: bool

    Проверяет учетку пользователя на активность
    """
    active_accounts = await get_all_active_accounts()
    active_emails = []
    for email in active_accounts:
        active_emails.append(email[1])

    if user_email in active_emails:
        return True
    else:
        return False


async def get_username_from_ad(user_email) -> str:
    """
    :param user_email:
    :return: str

    Возвращает актуальное имя из AD
    """
    active_accounts = await get_all_active_accounts()
    for email in active_accounts:
        if user_email == email[1]:
            return email[0]
        else:
            continue
