### For cascade dropdown FROM https://github.com/PrettyPrinted/dynamic_select_flask_wtf_javascript
from flask import jsonify
from flask_wtf import FlaskForm 
from wtforms import SelectField
### For cascade dropdown FROM https://github.com/PrettyPrinted/dynamic_select_flask_wtf_javascript




### FROM https://www.youtube.com/watch?v=I2dJuNwlIH0&feature=youtu.be
### FROM https://github.com/PrettyPrinted/dynamic_select_flask_wtf_javascript

@app.route('/', methods=['GET', 'POST'])
def dsply_dst_form():
    dst_form = Dst_form()
    dst_form.ar_form.choices = [(ar.id, ar.title) for ar in Age_range.query.all()]
    dst_form.tag_form.choices = [(tag.id, tag.title) for tag in Tag.query.all()]
    dst_form.scrt_form.choices = [(scrt.id, scrt.title) for scrt in Scrt.query.all()]

    if request.method == 'POST':
        ar = Age_range.query.filter_by(id=dst_form.ar.data).first()
        return '<h1>AR: {}, TAG: {}, SCRT: {}</h1>'.format(dst_form.ar.data, tag.name)

    return render_template('dsply_dst_form.destination_add.html', dst_form=dst_form)

                                            
@app.route('/tag_form')
def tag_form():
    tags = Tag.query.all()

    tagArray = []

    for tag in tags:
        tagObj = {}
        tagObj['id'] = tag.id
        tagObj['name'] = tag.title
        tagArray.append(tagObj)

    return jsonify({'tags' : tagArray})


### FROM https://www.youtube.com/watch?v=I2dJuNwlIH0&feature=youtu.be
### FROM https://github.com/PrettyPrinted/dynamic_select_flask_wtf_javascript
