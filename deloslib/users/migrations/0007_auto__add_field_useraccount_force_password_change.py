# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UserAccount.force_password_change'
        db.add_column(u'users_useraccount', 'force_password_change',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'UserAccount.force_password_change'
        db.delete_column(u'users_useraccount', 'force_password_change')


    models = {
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'users.contact': {
            'Meta': {'object_name': 'Contact'},
            'answer': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'answer_person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.UserAccount']", 'null': 'True', 'blank': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail_from': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'mail_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'msg': ('django.db.models.fields.TextField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '1'})
        },
        u'users.delosapplication': {
            'Meta': {'object_name': 'DelosApplication'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'users.delossite': {
            'Meta': {'object_name': 'DelosSite'},
            'custom_menu': ('django.db.models.fields.TextField', [], {}),
            'delos_apps': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['users.DelosApplication']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']", 'unique': 'True'})
        },
        u'users.role': {
            'Meta': {'object_name': 'Role'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.DelosApplication']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.UserAccount']"}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'unidade': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Unidade']"})
        },
        u'users.unidade': {
            'Meta': {'object_name': 'Unidade'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'cnpj': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'users.useraccount': {
            'Meta': {'ordering': "('name',)", 'object_name': 'UserAccount'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '550', 'null': 'True'}),
            'force_password_change': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identification': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.DelosApplication']", 'null': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'nro_usp': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'old_person_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'old_user_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'unidade': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Unidade']", 'null': 'True'})
        }
    }

    complete_apps = ['users']