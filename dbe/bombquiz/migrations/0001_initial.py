# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Question'
        db.create_table('bombquiz_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('order', self.gf('django.db.models.fields.IntegerField')(unique=True)),
        ))
        db.send_create_signal('bombquiz', ['Question'])

        # Adding model 'PlayerRecord'
        db.create_table('bombquiz_playerrecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=120)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('bombquiz', ['PlayerRecord'])

        # Adding unique constraint on 'PlayerRecord', fields ['name', 'email']
        db.create_unique('bombquiz_playerrecord', ['name', 'email'])

        # Adding model 'Answer'
        db.create_table('bombquiz_answer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('player_record', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answers', to=orm['bombquiz.PlayerRecord'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answers', to=orm['bombquiz.Question'])),
            ('correct', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('bombquiz', ['Answer'])

        # Adding unique constraint on 'Answer', fields ['question', 'player_record']
        db.create_unique('bombquiz_answer', ['question_id', 'player_record_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Answer', fields ['question', 'player_record']
        db.delete_unique('bombquiz_answer', ['question_id', 'player_record_id'])

        # Removing unique constraint on 'PlayerRecord', fields ['name', 'email']
        db.delete_unique('bombquiz_playerrecord', ['name', 'email'])

        # Deleting model 'Question'
        db.delete_table('bombquiz_question')

        # Deleting model 'PlayerRecord'
        db.delete_table('bombquiz_playerrecord')

        # Deleting model 'Answer'
        db.delete_table('bombquiz_answer')


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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
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
