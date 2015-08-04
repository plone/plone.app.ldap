# -*- coding: utf-8 -*-
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from zope.component import getUtility
from plone.app.ldap.engine.interfaces import ILDAPConfiguration
import ldap

from zope.schema.interfaces import IVocabularyFactory


class LDAPServerTypeVocabulary(object):
    """Vocabulary factory for LDAP server types.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        return SimpleVocabulary([
            SimpleTerm(u'LDAP', u'LDAP'),
            SimpleTerm(u'AD', u'Active Directory'),
        ])

LDAPServerTypeVocabularyFactory = LDAPServerTypeVocabulary()


class LDAPConnectionTypeVocabulary(object):
    """Vocabulary factory for LDAP connection types.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        return SimpleVocabulary([
            SimpleTerm(0, u'LDAP'),
            SimpleTerm(1, u'LDAP over SSL'),
            SimpleTerm(2, u'LDAP over IPC'),
        ])

LDAPConnectionTypeVocabularyFactory = LDAPConnectionTypeVocabulary()


class LDAPScopeVocabulary(object):
    """Vocabulary factory for LDAP search scopes.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        return SimpleVocabulary([
            SimpleTerm(ldap.SCOPE_ONELEVEL, u'one level'),
            SimpleTerm(ldap.SCOPE_SUBTREE, u'subtree'),
        ])

LDAPScopeVocabularyFactory = LDAPScopeVocabulary()


class LDAPAttributesVocabulary(object):
    """Vocabulary factory for LDAP attributes.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        config = getUtility(ILDAPConfiguration)
        attributes = [(a.ldap_name, a.__name__) for a in config.schema.values()]
        return SimpleVocabulary.fromItems(sorted(attributes))

LDAPAttributesVocabularyFactory = LDAPAttributesVocabulary()


class LDAPSingleValueAttributesVocabulary(object):
    """Vocabulary factory for LDAP attributes.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        config = getUtility(ILDAPConfiguration)
        attributes = [(a.ldap_name, a.__name__) for a in config.schema.values()
                    if not a.multi_valued]
        return SimpleVocabulary.fromItems(sorted(attributes))

LDAPSingleValueAttributesVocabularyFactory = LDAPSingleValueAttributesVocabulary()


class LDAPPasswordEncryptionVocabulary(object):
    """Vocabulary factory for LDAP Password encryption.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        return SimpleVocabulary([
            SimpleTerm('crypt', u'crypt'),
            SimpleTerm('SHA', u'SHA'),
            SimpleTerm('SSHA', u'SSHA'),
            SimpleTerm('md5', u'md5'),
            SimpleTerm('clear', u'clear'),
        ])

LDAPPasswordEncryptionVocabularyFactory = LDAPPasswordEncryptionVocabulary()
