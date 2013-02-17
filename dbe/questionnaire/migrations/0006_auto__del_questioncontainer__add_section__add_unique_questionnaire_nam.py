# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'QuestionContainer'
        db.delete_table('questionnaire_questioncontainer')

        # Adding model 'Section'
        db.create_table('questionnaire_section', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('questionnaire', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='sections', null=True, to=orm['questionnaire.Questionnaire'])),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('questionnaire', ['Section'])

        # Adding unique constraint on 'Questionnaire', fields ['name']
        db.create_unique('questionnaire_questionnaire', ['name'])

        # Deleting field 'Question.question_container'
        db.delete_column('questionnaire_question', 'question_container_id')

        # Adding field 'Question.section'
        db.add_column('questionnaire_question', 'section', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='questions', null=True, to=orm['questionnaire.Section']), keep_default=False)

        # Adding unique constraint on 'Question', fields ['section', 'order']
        db.create_unique('questionnaire_question', ['section_id', 'order'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Question', fields ['section', 'order']
        db.delete_unique('questionnaire_question', ['section_id', 'order'])

        # Removing unique constraint on 'Questionnaire', fields ['name']
        db.delete_unique('questionnaire_questionnaire', ['name'])

        # Adding model 'QuestionContainer'
        db.create_table('questionnaire_questioncontainer', (
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('questionnaire', self.gf('django.db.models.fields.related.ForeignKey')(related_name='containers', null=True, to=orm['questionnaire.Questionnaire'], blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
        ))
        db.send_create_signal('questionnaire', ['QuestionContainer'])

        # Deleting model 'Section'
        db.delete_table('questionnaire_section')

        # Adding field 'Question.question_container'
        db.add_column('questionnaire_question', 'question_container', self.gf('django.db.models.fields.related.ForeignKey')(related_name='questions', null=True, to=orm['questionnaire.QuestionContainer'], blank=True), keep_default=False)

        # Deleting field 'Question.section'
        db.delete_column('questionnaire_question', 'section_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'questionnaire.answer': {
            'Meta': {'ordering': "['question__section__order', 'question__order']", 'object_name': 'Answer'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'answers'", 'null': 'True', 'to': "orm['questionnaire.Question']"}),
            'user_questionnaire': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'answers'", 'null': 'True', 'to': "orm['questionnaire.UserQuestionnaire']"})
        },
        'questionnaire.question': {
            'Meta': {'ordering': "['order']", 'unique_together': "(['section', 'order'],)", 'object_name': 'Question'},
            'answer_type': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'choices': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'questions'", 'null': 'True', 'to': "orm['questionnaire.Section']"})
        },
        'questionnaire.questionnaire': {
            'Meta': {'object_name': 'Questionnaire'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'})
        },
        'questionnaire.section': {
            'Meta': {'ordering': "['order']", 'object_name': 'Section'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'questionnaire': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sections'", 'null': 'True', 'to': "orm['questionnaire.Questionnaire']"})
        },
        'questionnaire.userquestionnaire': {
            'Meta': {'ordering': "['user', 'created']", 'object_name': 'UserQuestionnaire'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'questionnaire': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_questionnaires'", 'null': 'True', 'to': "orm['questionnaire.Questionnaire']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'questionnaires'", 'null': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['questionnaire']
