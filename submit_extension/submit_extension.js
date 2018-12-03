// file submit_extension/main.js

// Needs to be changed on a class by class basis
grading_url = 'http://localhost:8000/services/gofer_nb/'
define([
    'base/js/namespace'
], function(
    Jupyter
) {
    function load_ipython_extension() {

        var handler = function () {
            var nb = Jupyter.notebook.toJSON(); // get the ipynb file
            // TODO:  strip the output to send less data
            // TODO:  see if test glob can also be encoded in metadata
            // assignment can be set by using notebook metadata
            // for now it's by hand
            lab = "test";
            payload = JSON.stringify({'assignment': lab, 'nb': nb});
            otherParam = {
                headers: {"Content-Type": "application/json"},
                body: payload,
                method: "POST"
            };
            /*  Example of filtering code cells
                cells = cells.filter(function(c) {return c instanceof IPython.CodeCell;}) */


            console.log(nb)
            console.log(otherParam)
            console.log(grading_url)
            alert("Submitted assignment to Gofer. Close this window, and your grade will be returned when it's finished running!")

            fetch(grading_url, otherParam)
                // processes the response (in this case grabs json)
                .then(response=>{return response.json()})
                // processes the output of previous line (calling it data, then doing something with it)
                .then(data=>{console.log( data); alert('Assignment grade is: ' + Math.round(100 * data).toString() + '%')});
                // .then(response=>{console.log(response.body.getReader().read())});
                // .then(response=>{grade = response.text().result; console.log(grade)});
                // .then(function(resp){r = resp; console.log(resp)})
                // .then(data=>{console.log( data.json())})
                // .catch(error=>{console.log(error)})
            // var json = await response.json();
            // console.log(json);

            // alert('grade is: ' + grade);
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
