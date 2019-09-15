$(document).ready(function () {
  // Class names

  // Class of button triggering formset management
  var buttonClass = 'dfs-button';
  // Class of element wrapping a form in a formset
  var formWrapperClass = 'dfs-form';
  // Class of element holding formset data in a data attributes
  var formsetInfoClass = 'dfs-formset-info';


  // Attribute names

  // Attribute to hold a formset prefix
  var formsetPrefixAttribute = 'data-dfs-formset-prefix';
  // Attribute to flag last form should always be optional
  var formsetLastFormOptionalAttribute = 'data-dfs-last-form-optional';
  // Attribute to flag removal of last form after cloning
  var formsetRemoveLastFormAttribute = 'data-dfs-remove-last-form';
  // Attribute to flag button as a permanent add button
  var addOnlyAttribute = 'data-dfs-action-add';
  // Attribute to specify how a new form should be inserted
  var insertionTypeAttribute = 'data-dfs-insertion-type';
  // Attribute to hold selector of element relative to which a new form will be inserted
  var insertionSelectorAttribute = 'data-dfs-insertion-selector';
  // Attribute to flag button as a remove button
  var removeOnlyAttribute = 'data-dfs-action-remove';
  // Attribute to hold prefix of form to remove
  var formPrefixAttribute = 'data-dfs-form-prefix';
  // Attribute to hold class name to add to removed forms
  var addClassAttribute = 'data-dfs-add-class';
  // Attribute to hold class name to remove from removed forms
  var removeClassAttribute = 'data-dfs-remove-class';


  // Variables

  var formsets = {};


  // Start main execution

  console.log('%cDjanky Formsets v1.0.0\nStarting djankurbation...', 'font-weight: bold;');


  // Retrieve template forms for each formset

  // Get formset prefixes from document
  $('.' + formsetInfoClass).map(function () {
    var formsetPrefix = $(this).attr(formsetPrefixAttribute);
    // Store formset info if prefix defined
    if (formsetPrefix !== undefined) {
      console.log('Retrieved formset prefix "' + formsetPrefix + '" from element with class "' + formsetInfoClass + '".');
      formsets[formsetPrefix] = {
        // Array of indices of deleted initial forms
        inactiveIndices: [],
        requiredFields: [],
        lastOptional: $(this).attr(formsetLastFormOptionalAttribute) !== undefined ? true : false,
        removeLast: $(this).attr(formsetRemoveLastFormAttribute) !== undefined ? true : false,
      };
    } else {
      console.warn('WARNING: Element with class "' + formsetInfoClass + '" has no attribute "' + formsetPrefixAttribute + '".');
    }
  });

  // Clone last form of each formset as template for new forms
  if (Object.keys(formsets).length) {
    $.each(formsets, function (formsetPrefix, formset) {
      // Form must have its formset prefix stored in the formset prefix attribute
      var form = $(formSelector(formsetPrefix)).last();
      if (form.length) {
        // Save list of required fields with formset info
        form.find(fieldSelector(formsetPrefix) + '[required]').each(function () {
          formset.requiredFields.push(parseFieldId($(this).attr('id')).fieldName);
        });
        // Store clone in dummy element so the outer HTML can be retrieved later
        formset.template = $('<div></div>').append(form.clone());
        // Remove form and decrement total in management form if specified
        formset.removeLast && form.remove() && incrementTotal(formsetPrefix, false);
        // Set or remove required attributes as necessary for all forms in formset
        manageRequiredForms(formsetPrefix);
      } else {
        console.error('ERROR: No element with class "' + formWrapperClass + '" and attribute "' + formsetPrefixAttribute + '="' + formsetPrefix + '"".');
      }
    });
  } else {
    console.error('ERROR: No elements with class "' + formsetInfoClass + '" and attribute "' + formsetPrefixAttribute + '".');
    return false;
  }


  // Helper functions
  // Management form getters return undefined if formset prefix invalid

  // Get total number of forms with specified formset prefix from management form
  function getTotal(formsetPrefix) {
    return parseInt($('#id_' + formsetPrefix + '-TOTAL_FORMS').val());
  }


  function setTotal(prefix, total) {
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
  }



  // Increment in specified direction total number of forms with specified formset prefix in management form
  function incrementTotal(formsetPrefix, up) {
    var totalElement = $('#id_' + formsetPrefix + '-TOTAL_FORMS');
    totalElement.val(parseInt(totalElement.val()) + (up ? 1 : -1));
  }

  // Get initial number of forms with specified formset prefix from management form
  function getInitial(formsetPrefix) {
    return parseInt($('#id_' + formsetPrefix + '-INITIAL_FORMS').val());
  }

  // Get minimum number of forms with specified formset prefix from management form
  function getMinNum(formsetPrefix) {
    return parseInt($('#id_' + formsetPrefix + '-MIN_NUM_FORMS').val());
  }

  // Get maximum number of forms with specified formset prefix from management form
  function getMaxNum(formsetPrefix) {
    return parseInt($('#id_' + formsetPrefix + '-MAX_NUM_FORMS').val());
  }

  // Return a selector for a form wrapper with the given formset prefix
  function formSelector(formsetPrefix) {
    return '.' + formWrapperClass + '[' + formsetPrefixAttribute + '="' + formsetPrefix + '"]';
  }

  // Return a selector for a field with the specified formset prefix, optional form index and optional field name
  function fieldSelector(formsetPrefix, formIndex, fieldName) {
    var selector = '[id^="id_' + formsetPrefix + '-';
    formIndex !== undefined && (selector += formIndex + '-');
    fieldName !== undefined && (selector += fieldName);
    return selector + '"][name]';
  }

  // Return a selector for a label of field with specified formset prefix and optional form index
  function labelSelector(formsetPrefix, formIndex) {
    var selector = 'label[for^="id_' + formsetPrefix + '-';
    formIndex !== undefined && (selector += formIndex + '-');
    return selector + '"]';
  }

  // Replace form index in specified string with specified index
  function replaceIndex(string, index) {
    return string.replace(/-[0-9]+-/, '-' + index + '-');
  }

  // Set fields of specified form as required or optional
  function setFormRequired(formsetPrefix, i, required) {
    $.each(formsets[formsetPrefix].requiredFields, function (index, fieldName) {
      required ? $(fieldSelector(formsetPrefix, i, fieldName)).attr('required', '') : $(fieldSelector(formsetPrefix, i, fieldName)).removeAttr('required');
    });
  }

  // Set relevant required attributes on fields of all forms in formset
  // Only forms with a form index less than current (total - 1) will be reached
  function manageRequiredForms(formsetPrefix) {
    var total = getTotal(formsetPrefix);
    var formset = formsets[formsetPrefix];
    var inactiveIndices = formset.inactiveIndices;

    // Last form is optional if specified and formset minimum allows
    var lastOptional = formset.lastOptional && (total - inactiveIndices.length > getMinNum(formsetPrefix));

    for (var i = total - 1, foundFinal = false; i >= 0; i--) {
      if ($.inArray(i, inactiveIndices) > -1) {
        // Remove required attribute from inactive forms
        setFormRequired(formsetPrefix, i, false);
      } else if (lastOptional && !foundFinal) {
        // Remove required attribute from final active form if optional
        setFormRequired(formsetPrefix, i, false);
        // Set flag to indicate final active form has been found
        foundFinal = true;
      } else {
        // Apply required attribute to all other forms
        setFormRequired(formsetPrefix, i, true);
      }
    }
  }

  // Update identifying attributes of specified fields and labels with specified index
  function updateFormIndices(fields, labels, index) {
    fields.each(function () {
      var name = replaceIndex($(this).attr('name'), index);
      var id = 'id_' + name;
      $(this).attr({ 'name': name, 'id': id });
    });
    labels.each(function () {
      var labelFor = replaceIndex($(this).attr('for'), index);
      $(this).attr('for', labelFor);
    });
  }

  // Return an object containing the formset prefix, form index and field name parsed from the specified field id string
  function parseFieldId(fieldId) {
    var re = /id_(.+)-(\d+)-(.+)/;
    return {
      formsetPrefix: fieldId.replace(re, '$1'),
      formIndex: fieldId.replace(re, '$2'),
      fieldName: fieldId.replace(re, '$3'),
    };
  }


  // Formset manipulation

  // Add form at specified position in formset specified by formset prefix
  function addForm(formsetPrefix, insertionSelector, insertionType) {
    var total = getTotal(formsetPrefix);
    if (total === undefined) {
      console.error('ERROR: No formset exists with prefix "' + formsetPrefix + '".');
      return false;
    }

    var formset = formsets[formsetPrefix];

    // Return from function if formset already has maximum number of forms
    var totalActive = total - formset.inactiveIndices.length;
    if (totalActive >= getMaxNum(formsetPrefix)) {
      console.log('Maximum number of active forms in formset "' + formsetPrefix + '" reached: ' + totalActive + '.');
      return false;
    }

    // Retrieve form template or return from function if template does not exist
    var form = formset.template;
    if (form === undefined) {
      console.error('ERROR: No element with class "' + formWrapperClass + '" and attribute "' + formsetPrefixAttribute + '="' + formsetPrefix + '"".');
      return false;
    }

    // Update identifying attributes of form
    updateFormIndices(form.find(fieldSelector(formsetPrefix)), form.find(labelSelector(formsetPrefix)), total);

    // Check specified selector is valid
    elements = $(insertionSelector);
    if (elements.length) {
      // Add form to document
      // If specified selector returns multiple elements, last element used
      switch (insertionType) {
        case 'before':
          elements.last().before(form.html());
          break;
        case 'prependToContent':
          elements.last().prepend(form.html());
          break;
        case 'replaceContent':
          elements.last().html(form.html());
          break;
        case 'appendToContent':
          elements.last().append(form.html());
          break;
        case 'after':
        default:
          elements.last().after(form.html());
          break;
      }
    } else {
      console.error('ERROR: No element matching selector "' + insertionSelector + '".\n\tPlease define a valid "' + insertionSelectorAttribute + '" attribute on this button.')
      return false;
    }

    // Increment total forms in management form
    incrementTotal(formsetPrefix, true);

    // Set or remove required attributes as necessary for all forms in formset
    manageRequiredForms(formsetPrefix);
    return true;
  }

  // Remove closest containing form of formset specified by formset prefix
  function removeForm(element, formsetPrefix, addClass, removeClass) {
    var total = getTotal(formsetPrefix);
    if (total === undefined) {
      console.error('ERROR: No formset exists with prefix "' + formsetPrefix + '".');
      return false;
    }

    var formset = formsets[formsetPrefix];

    // Return from function if formset already has minimum number of forms
    var totalActive = total - formset.inactiveIndices.length;
    if (totalActive <= getMinNum(formsetPrefix)) {
      console.log('Minimum number of active forms in formset "' + formsetPrefix + '" reached: ' + totalActive + '.');
      return false;
    }

    // Find closest containing form of element with specified formset prefix
    var form = element.closest(formSelector(formsetPrefix));
    var formIndex;
    if (form.length) {
      // Get form index
      var fields = form.find(fieldSelector(formsetPrefix));
      if (fields.length) {
        formIndex = parseInt(parseFieldId(fields.first().attr('id')).formIndex);
      } else {
        console.error('ERROR: Form contains no fields.');
        return false;
      }
    } else {
      console.error('ERROR: No containing element with class "' + formWrapperClass + '" and attribute "' + formsetPrefixAttribute + '".');
      return false;
    }

    // Add and remove specified classes or hide if classes undefined
    if (addClass === undefined && removeClass === undefined) {
      form.css('display', 'none');
    } else {
      form.removeClass(removeClass).addClass(addClass);
    }

    // Remove identifying attributes from form if extra or mark for deletion if initial
    if (formIndex > getInitial(formsetPrefix) - 1) {
      // This is an extra form; Remove identifying attributes
      // Remove required attribute here since form unreachable once id removed
      form.find(fieldSelector(formsetPrefix)).removeAttr('name id required');
      form.find(labelSelector(formsetPrefix)).removeAttr('for');

      // Decrement identifying attributes of following forms
      for (var i = formIndex + 1; i < total; i++) {
        updateFormIndices($(fieldSelector(formsetPrefix, i)), $(labelSelector(formsetPrefix, i)), i - 1);
      }

      // Decrement total forms in management form
      incrementTotal(formsetPrefix, false);
      console.log('Removed extra form ' + formIndex + ' from formset "' + formsetPrefix + '".');
    } else {
      // This is an initial form; Mark for deletion with Django form deletion checkbox
      var name = formsetPrefix + '-' + formIndex + '-DELETE';
      var id = 'id_' + name;
      // Check checkbox or create and append to management form if does not exist
      var deleteCheckbox = $('#' + id);
      if (deleteCheckbox === undefined) {
        $('#id_' + formsetPrefix + '-MAX_NUM_FORMS').after($('<input type="checkbox">').attr({ 'name': name, 'id': id }).css('display', 'none').prop('checked', true));
      } else {
        deleteCheckbox.prop('checked', true);
      }
      console.log('Marked initial form ' + formIndex + ' of formset "' + formsetPrefix + '" for deletion.');
      // Add form index to formset inactive form indices
      formset.inactiveIndices.push(formIndex);
    }

    // Set or remove required attributes as necessary for all forms in formset
    manageRequiredForms(formsetPrefix);
    return true;
  }


  // Event handlers

  $(document).on('click', '.' + buttonClass, function () {
    // Prefix of formset to modify is required
    var formsetPrefix = $(this).attr(formsetPrefixAttribute);
    if (formsetPrefix === undefined) {
      console.error('ERROR: No attribute "' + formsetPrefixAttribute + '" defined on this button.');
      return false;
    }

    // Whether button is always for adding forms
    // If neither addOnly nor removeOnly is set, button is initially an add button and changes to a remove button on click
    // Set to true if attribute is set, false if not
    var addOnly = ($(this).attr(addOnlyAttribute) !== undefined) ? true : false;

    // Selector of element relative to which a new form will be inserted
    // Defaults to form wrapper class with formset prefix attribute if not set
    var insertionSelector = $(this).attr(insertionSelectorAttribute);
    insertionSelector === undefined && (insertionSelector = formSelector(formsetPrefix));

    // Type of insertion as a string
    // addForm() handles undefined case
    var insertionType = $(this).attr(insertionTypeAttribute);

    // Whether button is for removing forms
    // Set to true if attribute is set, false if not
    var removeOnly = ($(this).attr(removeOnlyAttribute) !== undefined) ? true : false;

    // Prefix of individual form to remove
    var formPrefix = $(this).attr(formPrefixAttribute);
    // Used to find child element of form to remove
    // Defaults to button if not set
    var element = (formPrefix === undefined) ? $(this) : $(fieldSelector(formPrefix));

    // Class to add to removed forms
    var addClass = $(this).attr(addClassAttribute);

    // Class to remove from removed forms
    var removeClass = $(this).attr(removeClassAttribute);

    // Manipulate formset
    if (removeOnly) {
      if (addOnly) {
        // Log error if both addOnly and removeOnly
        console.error('ERROR: Button has both attributes "' + addOnlyAttribute + '" and "' + removeOnlyAttribute + '".\n\tOnly one of these attributes is permitted.');
        return false;
      } else {
        // Remove form
        console.log('Removing form from formset "' + formsetPrefix + '"...');
        if (!removeForm(element, formsetPrefix, addClass, removeClass)) {
          console.log('Failed to remove form from formset "' + formsetPrefix + '".');
          return false;
        }
      }
    } else {
      // Add form
      console.log('Adding form to formset "' + formsetPrefix + '"...');
      if (!addForm(formsetPrefix, insertionSelector, insertionType)) {
        console.log('Failed to add form to formset "' + formsetPrefix + '".');
        return false;
      }
      // Change add button to remove button if not addOnly
      if (!addOnly) {
        console.log('Adding attribute "' + removeOnlyAttribute + '" to button...');
        $(this).attr(removeOnlyAttribute, '');
      }
    }

    // Form management successful
    console.log('Operation completed.');
    return true;
  });
});
