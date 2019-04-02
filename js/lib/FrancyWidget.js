var widgets = require('@jupyter-widgets/base');
var widgets = require('@jupyter-widgets/controls');
var _ = require('lodash');

var FrancyModel = widgets.StringModel.extend({
    defaults: _.extend(widgets.StringModel.prototype.defaults(), {
        _model_name : 'FrancyModel',
        _view_name : 'FrancyView',
        _model_module : 'sage-francy',
        _view_module : 'sage-francy',
        _model_module_version : '0.1.0',
        _view_module_version : '0.1.0',
        value : 'Francy Widget'
    })
});

var FrancyView = widgets.DescriptionView.extend({
    render: function() {
        widgets.StringView.prototype.render.call(this);
        this.el.classList.add('jupyter-widgets');
        this.el.classList.add('widget-inline-hbox');
        this.el.classList.add('widget-francy');
        this.content = document.createElement('div');
        this.content.classList.add('widget-francy-content');
        this.el.appendChild(this.content);
        this.update(); // Set defaults.
    },

    /**
     * Update the contents of this view
     */
    update: function() {
        this.content.innerHTML = this.model.get('value');
        this.typeset(this.content);
        return widgets.StringView.prototype.update.call(this);
    }
});

module.exports = {
    FrancyModel : FrancyModel,
    FrancyView : FrancyView
};
