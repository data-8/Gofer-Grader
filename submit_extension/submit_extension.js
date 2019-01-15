// file submit_extension/main.js

// Needs to be changed on a class by class basis

grading_url = '/services/gofer_nb/'
define([
    'base/js/namespace'
], function(
    Jupyter
) {
    function load_ipython_extension() {

        var handler = function () {
            var nb = Jupyter.notebook.toJSON(); // get the ipynb file
            // TODO:  strip the output to send less data
            payload = JSON.stringify({'nb': nb});
            otherParam = {
                headers: {"Content-Type": "application/json"},
                body: payload,
                method: "POST"
            };

            fetch(grading_url, otherParam)
                // processes the response (in this case grabs text)
                .then(response=>{return response.text()})
                // processes the output of previous line (calling it data, then doing something with it)
                .then(data=>{console.log( data); alert(data)});
        };

        var action = {
            icon: 'fa-check', // a font-awesome class used on buttons, etc
            label: 'Submit',
            help    : 'Submit assignment',
            help_index : 'zz',
            handler : handler
        };
        var prefix = 'Gofer';
        var action_name = 'submit';

        var full_action_name = Jupyter.actions.register(action, action_name, prefix); // returns 'Gofer:submit'
        // Jupyter.toolbar.add_buttons_group([full_action_name]);
        Jupyter.toolbar.add_buttons_group([
            {
                'label' : 'Submit',
                'icon' : 'fa-check',
                'callback': handler
            }]);

    }

    return {
        load_ipython_extension: load_ipython_extension
    };
});
