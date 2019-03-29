var sage-francy = require('./index');
var base = require('@jupyter-widgets/base');

module.exports = {
  id: 'sage-francy',
  requires: [base.IJupyterWidgetRegistry],
  activate: function(app, widgets) {
      widgets.registerWidget({
          name: 'sage-francy',
          version: sage-francy.version,
          exports: sage-francy
      });
  },
  autoStart: true
};

