var widgets = require('@jupyter-widgets/base');
var widgets = require('@jupyter-widgets/controls');
var _ = require('lodash');

var FrancyView = widgets.HTMLView.extend({
    render: function() {
        widgets.HTMLView.prototype.render.call(this);
    }
});

module.exports = {
    FrancyView : FrancyView
};
