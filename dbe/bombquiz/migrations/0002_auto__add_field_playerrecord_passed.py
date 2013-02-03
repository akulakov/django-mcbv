# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'PlayerRecord.passed'
        db.add_column('bombquiz_playerrecord', 'passed', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'PlayerRecord.passed'
        db.delete_column('bombquiz_playerrecord', 'passed')


    models = {
        'bombquiz.answer': {
            'Meta': {'ordering': "['question__order']", 'unique_together': "[['question', 'player_record']]", 'object_name': 'Answer'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'correct': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player_record': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': "orm['bombquiz.PlayerRecord']"}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': "orm['bombquiz.Question']"})
        },
        'bombquiz.playerrecord': {
            'Meta': {'ordering': "['created']", 'unique_together': "[['name', 'email']]", 'object_name': 'PlayerRecord'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '120'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'passed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'bombquiz.question': {
            'Meta': {'ordering': "['order']", 'object_name': 'Question'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['bombquiz']
