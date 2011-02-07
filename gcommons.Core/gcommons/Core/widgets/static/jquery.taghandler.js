/*
    jQuery Tag Handler v1.0.1
    Copyright (C) 2010 Mark Jubenville
    Mark Jubenville - ioncache@gmail.com
    http://ioncache.github.com/Tag-Handler
    
    Development time supported by:
    Raybec Communications
    http://www.raybec.com
    http://www.mysaleslink.com
    
    Modified by Javier Fernandez Escribano - fesjav@gmail.com
    Added autocomplete queries as the user writes

    Development time supported by:
    Tourist Eye
    http://www.touristeye.com

    Based heavily on:
    Tag it! by Levy Carneiro Jr (http://levycarneiro.com/)
    http://levycarneiro.com/projects/tag-it/example.html
    http://github.com/levycarneiro/tag-it
    http://plugins.jquery.com/project/tag-it

    Tag icons/cursors converted from:
    From the famfamfam.com Silk icon set:
    http://www.famfamfam.com/lab/icons/silk/
    
    Loader image created at:
    Preloaders.net
    http://preloaders.net/

    ----------------------------------------------------------------------------
    Description 
    ----------------------------------------------------------------------------

    Tag Handler is a jquery plugin used for managing tag-type metadata.
    
    Tag Handler must be attached to one or more <ul> tags in your HTML.

    To add a tag, click on the tag box, type in a name, and hit enter or comma.

    Tags may be removed from the tag box by hitting backspace or clicking on
    the tag.
    
    Tag Handler may receive a list of tags when initialized or by pulling data
    via ajax from a supplied URL. It may also post back a list of tags to a
    separately specified URL.
    
    If tags are retrieved with the a URL, the server must supply a JSON
    formatted string with an array titled 'availableTags' and optionally an
    array titled 'assignedTags'. The 'availableTags' array will populate the
    autocomplete list for the tag input field, and the list of 'assignedTags'
    will be added as tags to the tag container.

    If tags are updated via ajax, then an array of tags will be sent back to
    the updateURL named 'tags'.  You may also specify any additional data to
    be sent with the updateData option.
    
    A sample CSS file is included that can be used to help with formatting tags.

    ----------------------------------------------------------------------------
    Plugin Examples
    ----------------------------------------------------------------------------

    Example 1: The Tag Handler will be initialized with no options and no
               default tags:

        $("#tag_container").tagHandler();

    Example 2: The Tag Handler will be initialized with preset tags from the
               assignedTags and availableTags arrays, and autocomplete witll
               be turned on:
    
        $("#tag_container").tagHandler({
           assignedTags: [ 'Perl' ] ,
           availableTags: [ 'C', 'C++', 'C#', 'Java', 'Perl', 'PHP', 'Python' ],
           autocomplete: true
        });

    Example 3: The Tag Handler will be initialized and pull data via ajax,
               also sending some data to the server:

        $("#tag_container").tagHandler({
            getData: { 'id': user_id, 'type': 'user' },
            getURL: '/get_record_tags',
            autocomplete: true
        });

    ----------------------------------------------------------------------------
    Plugin Options
    ----------------------------------------------------------------------------

    Tag data options:
    assignedTags:  optional array to use for assignedTags: default: []
    availableTags: optional array to use for availableTags: default: []
    getData:       data field with info for getURL - default: ''
    getURL:        URL to get tag list via ajax - default: ''
    initLoad:      indicates whether load all tags at init or when requested - default: true
    updatetData:   data field with info for updateURL - default: ''
    updateURL:     URL to update tag list via ajax - default: ''
    
    Misc options:
    allowEdit:     indicates whether the tag list is editable - default: true
    allowAdd:      indicates whether the user can add new tags - default: true
    autocomplete:  requires jqueryui autocomplete plugin - default: false
    autoUpdate:    indicates whether updating occurs automatically whenever
                   a tag is added/deleted. If set true, the save button will
                   not be shown - default: false
    className:     class to add to all tags - default: 'tagHandler'
    queryname:     variable name to query the server - default: 'q'
    debug:         turns debugging on and off - default: false
    delimiter:     extra delimiter to use to separate tags - default: ''
                   Note: enter and comma are always allowed
    sortTags:      sets sorting of tag names alphabetically - default: true
    minChars:      minimun number of chars to query the server - default: 0
    messageNoPermissionNewTag: message shown when the user cannot add a new tag - default: "You don't have enough points to create a new tag",
    messageErrorLoading: message shown when there is an error loading the tags - default: "There was an error getting the tag list."
    
    ----------------------------------------------------------------------------
    To Do
    ----------------------------------------------------------------------------

    Error checking of some sort should be added to the ajax methods.

    ----------------------------------------------------------------------------
    License
    ----------------------------------------------------------------------------

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see < http://www.gnu.org/licenses/ >.

*/

(function($) {

    $.fn.tagHandler = function(options) {
        var opts = $.extend({}, $.fn.tagHandler.defaults, options);
        tagDebug($(this), opts);

        // processes each specified object and adds a tag handler to each
        return this.each(function() {
            // checks to make sure the supplied element is a <ul>
            if (!$(this).is('ul')) {
                next;
            }

            // adds an id to the tagContainer in case it doesn't have one
            if (!this.id) {
                var d = new Date();
                this.id = d.getTime();
            }

            var tagContainer = this;

            // wraps the <ul> element in a div mainly for use in positioning
            // the save button and loader image.
            $(tagContainer).wrap('<div class="' + opts.className + '" />');

            // adds the the tag class to the tagContainer and creates the tag
            // input field
            $(tagContainer).addClass(opts.className + "Container");
            if (opts.allowEdit) {
                $(tagContainer).html('<li class="tagInput"><input class="tagInputField" type="text" /></li>');
            }
            var inputField = $(tagContainer).find(".tagInputField");

            /* JG PATCH: autocomplete('options'...) below fail if autocomplete is not init first: */
            if (opts.autocomplete && opts.allowEdit) {
                $(inputField).autocomplete({ source:'', minLength: opts.minChars});
            }
            /* END PATCH */

            // master tag list, will contain 3 arrays of tags
            var tags = [];
            tags.availableTags = [];
            tags.originalTags = [];
            tags.assignedTags = [];

            // adds a save/loader divs to the tagContainer if needed
            if (opts.updateURL != '') {
                if (!opts.autoUpdate) {
                    $("<div />").attr({ id: tagContainer.id + "_save", title: "Save Tags" }).addClass("tagUpdate").click(function() {
                        saveTags(tags, opts, tagContainer.id);
                    }).appendTo($(tagContainer).parent());
                }
                $("<div />").attr({ id: tagContainer.id + "_loader", title: "Saving Tags" }).addClass("tagLoader").appendTo($(tagContainer).parent());
            }

            // initializes the tag lists
            // tag lists will be pulled from a URL
            if (opts.getURL != '' && opts.initLoad) {
                
                $.ajax({
                    url: opts.getURL,
                    cache: false,
                    data: opts.getData,
                    dataType: 'json',
                    success: function(data, text, xhr) {
                        if (data.availableTags.length) {
                            tags.availableTags = data.availableTags.slice();
                            tags.originalTags = tags.availableTags.slice();
                        }
                        if (opts.sortTags) {
                            tags = sortTags(tags);
                        }
                        if (data.assignedTags.length) {
                            tags.assignedTags = data.assignedTags.slice();
                            if (opts.sortTags) {
                                tags = sortTags(tags);
                            }     


                            // adds any already assigned tags to the tag box
                            for (var x = 0; x < tags.assignedTags.length; x++) {
                                if (opts.allowEdit) {
                                    $("<li />").addClass("tagItem").html(tags.assignedTags[x]).insertBefore($(inputField).parent());
                                } else {
                                    $("<li />").addClass("tagItem").css("cursor", "default").html(tags.assignedTags[x]).appendTo($(tagContainer));
                                }
                                tags.availableTags = removeTagFromList(tags.assignedTags[x], tags.availableTags);
                            }
                        }
                        if (opts.autocomplete && opts.allowEdit) {
                            $(inputField).autocomplete("option", "source", tags.availableTags);
                        }
                    },
                    error: function(xhr, text, error) {
                        alert(opts.messageErrorLoading);
                    }
                });              
            
            // show assigned tags only if we load the data as we write
            } else if( opts.getURL != '' ) {

                tags.assignedTags = opts.assignedTags.slice();
                if (opts.sortTags) {
                  tags = sortTags(tags);
                }

                // adds any already assigned tags to the tag box
                for (var x = 0; x < tags.assignedTags.length; x++) {
                  if (opts.allowEdit) {
                    $("<li />").addClass("tagItem").html(tags.assignedTags[x]).insertBefore($(inputField).parent());
                  } else {
                    $("<li />").addClass("tagItem").css("cursor", "default").html(tags.assignedTags[x]).appendTo($(tagContainer));
                  }
                }
                
            // or load the lists of tags   
            } else {
                
                if (opts.availableTags.length) {
                    tags.availableTags = opts.availableTags.slice();
                    tags.originalTags = tags.availableTags.slice();
                }
                if (opts.sortTags) {
                    tags = sortTags(tags);
                }  
                if (opts.assignedTags.length) {
                    tags.assignedTags = opts.assignedTags.slice();
                    if (opts.sortTags) {
                        tags = sortTags(tags);
                    }

                    // adds any already assigned tags to the tag box
                    for (var x = 0; x < tags.assignedTags.length; x++) {
                        if (opts.allowEdit) {
                            $("<li />").addClass("tagItem").html(tags.assignedTags[x]).insertBefore($(inputField).parent());
                        } else {
                            $("<li />").addClass("tagItem").css("cursor", "default").html(tags.assignedTags[x]).appendTo($(tagContainer));
                        }
                        tags.availableTags = removeTagFromList(tags.assignedTags[x], tags.availableTags);
                    }
                }
                if (opts.autocomplete && opts.allowEdit && opts.initLoad) {
                    $(inputField).autocomplete("option", "source", tags.availableTags);
                }
            }

            // all tag editing functionality only activated if set in options
            if (opts.allowEdit) {
                // delegates a click event function to all future <li> elements with
                // the tagItem class that will remove the tag upon click
                $(tagContainer).delegate("#" + this.id + " li.tagItem", "click",
                function() {
                    tags = removeTag($(this), tags, opts.sortTags);
                    if (opts.updateURL != '' && opts.autoUpdate) {
                        saveTags(tags, opts, tagContainer.id);
                    }
                    if (opts.autocomplete && opts.initLoad) {
                      $(inputField).autocomplete("option", "source", tags.availableTags);
                    }
                });

                // checks the keypress event for enter or comma, and adds a new tag
                // when either of those keys are pressed
                $(inputField).keypress(function(e) {
                    if (e.which == 13 || e.which == 44 || e.which == opts.delimiter.charCodeAt(0)) {
                        e.preventDefault();
                        if ($(this).val() != "" && !checkTag($.trim($(this).val()), tags.assignedTags)) {
                            
                            // check if the tag is in availableTags
                            if( !opts.allowAdd && !checkTag($.trim($(this).val()), tags.availableTags)){
                              alert(opts.messageNoPermissionNewTag);
                              return;
                            }
                            
                            tags = addTag(this, $.trim($(this).val()), tags, opts.sortTags);
                            if (opts.updateURL != '' && opts.autoUpdate) {
                                saveTags(tags, opts, tagContainer.id);
                            }
                            if (opts.autocomplete && opts.initLoad) {
                              $(inputField).autocomplete("option", "source", tags.availableTags);
                            }
                            $(this).val("");
                            $(this).focus();
                        }
                    }
                });

                // checks the keydown event for the backspace key as checking the
                // keypress event doesn't work in IE
                $(inputField).keydown(function(e) {
                    if (e.which == 8 && $(this).val() == "") {
                        tags = removeTag($(tagContainer).find(".tagItem:last"), tags, opts.sortTags);
                        if (opts.updateURL != '' && opts.autoUpdate) {
                            saveTags(tags, opts, tagContainer.id);
                        }
                        if (opts.autocomplete && opts.initLoad) {
                          $(inputField).autocomplete("option", "source", tags.availableTags);
                        }
                        $(this).focus();
                    }
                });

                // adds autocomplete functionality for the tag names
                if (opts.autocomplete && opts.initLoad) {
                    
                    $(inputField).autocomplete({
                        source: tags.availableTags,
                        select: function(event, ui) {
                            if (!checkTag($.trim(ui.item.value), tags.assignedTags)) {
                                tags = addTag(this, $.trim(ui.item.value), tags, opts.sortTags);
                                if (opts.updateURL != '' && opts.autoUpdate) {
                                    saveTags(tags, opts, tagContainer.id);
                                }
                                $(inputField).autocomplete("option", "source", tags.availableTags);
                                $(this).focus();
                            }
                            $(this).val("");
                            return false;
                        },
                        minLength: opts.minChars
                    });
                    
                // Make an AJAX request to get the list of tags
                }else if( opts.autocomplete ){
                
                    var cache = {};
                    
                    $(inputField).autocomplete({
                        minLength: opts.minChars,
                        source: function( request, response ) {
                          var term = request.term;
                          if ( term in cache ) {
                            response( cache[ term ] );
                            return;
                          }
                          // Add term to search on the server
                          opts.getData[opts.queryName] = term;
                          lastXhr = $.getJSON( opts.getURL, opts.getData, function( data, status, xhr ) {
                              cache[ term ] = data;
                              if ( xhr === lastXhr ) {
                                response( data );
                    	      }
                           });
                        },
                        select: function(event, ui) {
                            if (!checkTag($.trim(ui.item.value), tags.assignedTags)) {
                                tags = addTag(this, $.trim(ui.item.value), tags, opts.sortTags);
                                if (opts.updateURL != '' && opts.autoUpdate) {
                                    saveTags(tags, opts, tagContainer.id);
                                }
                                $(this).focus();
                            }
                            $(this).val("");
                            return false;
                        }
                    });
                }

                // sets the input field to show the autocomplete list on focus
                // when there is no value
                $(inputField).focus(function() {
                    if ($(inputField).val() == "" && opts.autocomplete && opts.initLoad) {
                        $(inputField).autocomplete("search", "");
                    }
                });

                // sets the focus to the input field whenever the user clicks
                // anywhere on the tagContainer -- since the input field by default
                // has no border it isn't obvious where to click to access it
                $(tagContainer).click(function() {
                    $(inputField).focus();
                });
            }
        });
    };

    // plugin option defaults
    $.fn.tagHandler.defaults = {
        allowEdit: true,
        allowAdd: true,
        assignedTags: [],
        autocomplete: false,
        autoUpdate: false,
        availableTags: [],
        className: 'tagHandler',
        queryName: 'q',
        debug: false,
        delimiter: '',
        getData: '',
        getURL: '',
        initLoad: true,
        sortTags: true,
        updatetData: '',
        updateURL: '',
        minChars: 0,
        messageNoPermissionNewTag: "You don't have enough points to create a new tag",
        messageErrorLoading: "There was an error getting the tag list."
    };
    
    // checks to to see if a tag is already found in a list of tags
    function checkTag(value, tags) {
        var check = false;
        for (var x = 0; x < tags.length; x++) {
            if (tags[x] == value) {
                check = true;
                break;
            }
        }

        return check;
    }

    // removes a tag from a tag list
    function removeTagFromList(value, tags) {
        for (var x = 0; x < tags.length; x++) {
            if (tags[x] == value) {
                tags.splice(x, 1);
            }
        }

        return tags;
    }

    // adds a tag to the tag box and the assignedTags list
    function addTag(tagField, value, tags, sort) {
        tags.assignedTags.push(value);
        tags.availableTags = removeTagFromList(value, tags.availableTags);
        $("<li />").addClass("tagItem").html(value).insertBefore($(tagField).parent());

        if (sort) {
            tags = sortTags(tags);
        }
        return tags;
    }

    // removes a tag from the tag box and the assignedTags list
    function removeTag(tag, tags, sort) {
        var value = $(tag).html();
        tags.assignedTags = removeTagFromList(value, tags.assignedTags);
        if (checkTag(value, tags.originalTags)) {
            tags.availableTags.push(value);
        }
        $(tag).remove();

        if (sort) {
            tags = sortTags(tags);
        }
        return tags;
    }

    // sorts each of the sets of tags
    function sortTags(tags) {
        tags.availableTags = tags.availableTags.sort();
        tags.assignedTags = tags.assignedTags.sort();
        tags.originalTags = tags.originalTags.sort();

        return tags;
    }

    // saves the tags to the server via ajax
    function saveTags(tags, opts, tcID) {
        sendData = {
            tags: tags.assignedTags
        };
        $.extend(sendData, opts.updateData);
        $.ajax({
            type: 'POST',
            url: opts.updateURL,
            cache: false,
            data: sendData,
            dataType: 'json',
            beforeSend: function() {
                if ($("#" + tcID + "_save").length) {
                    $("#" + tcID + "_save").fadeOut(200,
                    function() {
                        $("#" + tcID + "_loader").fadeIn(200);
                    });
                } else {
                    $("#" + tcID + "_loader").fadeIn(200);
                }
            },
            complete: function() {
                $("#" + tcID + "_loader").fadeOut(200,
                function() {
                    if ($("#" + tcID + "_save").length) {
                        $("#" + tcID + "_save").fadeIn(200);
                    }
                });
            }
        });
    }

    // some debugging information
    function tagDebug(tagContainer, options) {
        if (window.console && window.console.log && options.debug) {
            window.console.log(tagContainer);
            window.console.log(options);
            window.console.log($.fn.tagHandler.defaults);
        }
    }

})(jQuery);