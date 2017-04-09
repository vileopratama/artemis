# -*- coding: utf-8 -*-
import logging
from odoo import fields, models, _

_logger = logging.getLogger(__name__)


class Template(models.Model):
    _name = 'crm.prospective.client.template'
    _description = 'Prospective Client Template'
    _order = 'sequence,id'

    name = fields.Char('Template Title', required=True, translate=True)
    question_ids = fields.One2many(comodel_name='crm.prospective.client.template.question', inverse_name='template_id',
                                   string='Questions', copy=True)
    sequence = fields.Integer('Page number', default=10)
    description = fields.Html('Description', translate=True, oldname="note", help="An introductory template")


class Question(models.Model):
    _name = 'crm.prospective.client.template.question'
    _description = 'Question'
    _order = 'sequence asc'

    name = fields.Char('Question', required=True, translate=True)
    template_id = fields.Many2one(comodel_name='crm.prospective.client.template', string='Template', ondelete='cascade',
                                  required=True, default=lambda self: self.env.context.get('template_id'))
    sequence = fields.Integer(string='Sequence', default=10)
    description = fields.Html(string='Description', translate=True, oldname='descriptive_text')
    constr_mandatory = fields.Boolean(string='Mandatory Answer', oldname="is_require_answer")
    constr_error_msg = fields.Char('Error message', oldname='req_error_msg', translate=True,
                                   default=lambda self: _("This question requires an answer."))
    type = fields.Selection([
        ('free_text', 'Multiple Lines Text Box'),
        ('textbox', 'Single Line Text Box'),
        ('numerical_box', 'Numerical Value'),
        ('datetime', 'Date and Time'),
        ('simple_choice', 'Multiple choice: only one answer'),
        ('multiple_choice', 'Multiple choice: multiple answers allowed'),
        ('matrix', 'Matrix')], string='Type of Question', default='free_text', required=True)

    validation_email = fields.Boolean('Input must be an email')
    validation_required = fields.Boolean('Validate entry', oldname='is_validation_require')
    validation_length_min = fields.Integer('Minimum Text Length')
    validation_length_max = fields.Integer('Maximum Text Length')
    validation_min_float_value = fields.Float('Minimum value')
    validation_max_float_value = fields.Float('Maximum value')
    validation_min_date = fields.Datetime('Minimum Date')
    validation_max_date = fields.Datetime('Maximum Date')
    validation_error_msg = fields.Char('Validation Error message', oldname='validation_valid_err_msg',
                                       translate=True,
                                       default=lambda self: _("The answer you entered has an invalid format."))
    matrix_subtype = fields.Selection([('simple', 'One choice per row'),
                                       ('multiple', 'Multiple choices per row')], string='Matrix Type',
                                      default='simple')
    display_mode = fields.Selection([('columns', 'Radio Buttons'), ('dropdown', 'Selection Box')], default='columns')
    column_nb = fields.Selection([('12', '1'), ('6', '2'), ('4', '3'), ('3', '4'), ('2', '6')],
                                 string='Number of columns', default='12')
    comments_allowed = fields.Boolean(string='Show Comments Field', oldname="allow_comment")
    comments_message = fields.Char(string='Comment Message', translate=True,
                                   default=lambda self: _("If other, please specify:"))
    comment_count_as_answer = fields.Boolean(string='Comment Field is an Answer Choice',
                                             oldname='make_comment_field')
    answer_ids = fields.One2many(comodel_name='crm.prospective.client.template.answer', inverse_name='question_id',
                                 string='Types of answers',
                                 oldname='answer_choice_ids',
                                 copy=True)
    answer_ids_2 = fields.One2many(comodel_name='crm.prospective.client.template.answer', inverse_name='question_id_2',
                                   string='Rows of the Matrix', copy=True)

    _sql_constraints = [
        ('positive_len_min', 'CHECK (validation_length_min >= 0)', 'A length must be positive!'),
        ('positive_len_max', 'CHECK (validation_length_max >= 0)', 'A length must be positive!'),
        ('validation_length', 'CHECK (validation_length_min <= validation_length_max)',
         'Max length cannot be smaller than min length!'),
        ('validation_float', 'CHECK (validation_min_float_value <= validation_max_float_value)',
         'Max value cannot be smaller than min value!'),
        ('validation_date', 'CHECK (validation_min_date <= validation_max_date)',
         'Max date cannot be smaller than min date!')
    ]


class Answer(models.Model):
    _name = 'crm.prospective.client.template.answer'
    _rec_name = 'value'
    _order = 'sequence,id'
    _description = 'Question Answer'

    question_id = fields.Many2one('crm.prospective.client.template.question', string='Question', ondelete='cascade')
    question_id_2 = fields.Many2one('crm.prospective.client.template.question', string='Question 2', ondelete='cascade')
    sequence = fields.Integer('Sequence order', default=10)
    value = fields.Char('Suggested value', translate=True, required=True)
    quizz_mark = fields.Float('Score for this choice', help="A positive score indicates a correct choice")
