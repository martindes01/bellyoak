$(document).ready(function () {
  // TODO
  // Check for empty collections


  // Selectors

  // Selector for form field input elements
  var inputSelector = "input:not([type=button]):not([type=submit]):not([type=reset]), textarea";

  // Class of button triggering formset management
  var buttonClass = ".button-form-action";
  // Class of element wrapping a form in a formset
  var formWrapperClass = ".formset-form";
  // Class of element holding a formset prefix in a data attribute
  var prefixHolderClass = ".formset-prefix-holder";


  // Attributes

  // Attribute to hold a formset prefix
  var formsetPrefixAttribute = "data-formset-prefix";
  // Attribute to flag button as a permanent add button
  var addOnlyAttribute = "data-action-add";
  // Attribute to specify how a new form should be inserted
  var insertionTypeAttribute = "data-insertion-type";
  // Attribute to hold selector of element relative to which a new form will be inserted
  var insertionSelectorAttribute = "data-insertion-selector";
  // Attribute to flag button as a remove button
  var removeOnlyAttribute = "data-action-remove";
  // Attribute to store index of form to remove
  var removalIndexAttribute = "data-removal-index";
  // Attribute to store class name for removed forms
  var removedFormClassAttribute = "data-removed-form-class";


  // Variables

  var prefixes = [];
  var templates = {};


  // Retrieve template forms for each formset

  // Get formset prefixes from document
  $(prefixHolderClass).map(function () {
    var prefix = $(this).attr(formsetPrefixAttribute);
    // Do not store if undefined
    if (prefix !== undefined) {
      console.log("Retrieved prefix '" + prefix + "' from element with class '" + prefixHolderClass + "'.");
      prefixes.push(prefix);
    } else {
      console.log("ERROR:\n\tElement with class '" + prefixHolderClass + "' has no attribute '" + formsetPrefixAttribute + "'.");
    }
  });

  // CLone last form of each formset as template for new forms
  if (prefixes.length > 0) {
    // Form must have its formset prefix stored in the formset prefix attribute
    $.each(prefixes, function (index, prefix) {
      templates[prefix] = $("<div></div>").append($(formWrapperClass + "[" + formsetPrefixAttribute + "=\"" + prefix + "\"]").last().clone(true));
    });
  } else {
    // If prefixes not provided, save last form in document under Django default prefix "form"
    console.log("WARNING:\n\tNo elements with class '" + prefixHolderClass + "' and attribute '" + formsetPrefixAttribute + "'.\n\tUsing Django default prefix 'form' instead.");
    templates["form"] = $("<div></div>").append($(formWrapperClass).last().clone(true));
  }


  // Helper functions

  // Get total number of forms with specified prefix from management form
  // Returns undefined if prefix invalid
  function getTotal(prefix) {
    return $("#id_" + prefix + "-TOTAL_FORMS").val();
  }

  // Set total number of forms with specified prefix to management form
  function setTotal(prefix, total) {
    $("#id_" + prefix + "-TOTAL_FORMS").val(total);
  }

  // Get minimum number of forms with specified prefix from management form
  // Returns undefined if prefix invalid
  function getMinNum(prefix) {
    return $("#id_" + prefix + "-MIN_NUM_FORMS").val();
  }

  // Get maximum number of forms with specified prefix from management form
  // Returns undefined if prefix invalid
  function getMaxNum(prefix) {
    return $("#id_" + prefix + "-MAX_NUM_FORMS").val();
  }

  // Replace form index in specified string with specified index
  function replaceIndex(string, newIndex) {
    return string.replace(/-[0-9]+-/, "-" + newIndex + "-");
  }


  // Formset manipulation

  // Add form at specified position in formset specified by prefix
  function addForm(prefix, insertionSelector, insertionType) {
    // getTotal() returns undefined if prefix invalid
    var total = getTotal(prefix);
    if (total === undefined) {
      console.log("ERROR:\n\tNo formset exists with prefix '" + prefix + "'.");
      return false;
    }

    // Return if formset already has maximum number of forms
    // getMaxNum() will not return undefined here, since addForm() returns earlier if prefix invalid
    if (total >= getMaxNum(prefix)) {
      console.log("Maximum number of forms in formset '" + prefix + "' reached: " + total + ".");
      return false;
    }

    // Update name and id attributes of input elements
    templates[prefix].find(inputSelector).each(function () {
      var name = replaceIndex($(this).attr("name"), total);
      var id = "id_" + name;
      $(this).attr({ "name": name, "id": id });
    });

    // Update for attribute of labels
    templates[prefix].find("label").each(function () {
      var id = "id_" + replaceIndex($(this).attr("for"), total);
      $(this).attr("for", id);
    });

    // Check specified selector is valid
    elements = $(insertionSelector);
    if (elements === undefined) {
      console.log("ERROR:\n\tCould not find element matching selector '" + insertionSelector + "'.\n\tPlease define a valid '" + insertionSelectorAttribute + "' attribute on this button.")
      return false;
    } else {
      // Add form to document
      // If specified selector returns multiple elements, last element used
      // Default insertion type is after element
      switch (insertionType) {
        case "before":
          elements.last().before(templates[prefix].html());
          break;
        case "prependToContent":
          elements.last().prepend(templates[prefix].html());
          break;
        case "replaceContent":
          elements.last().html(templates[prefix].html());
          break;
        case "appendToContent":
          elements.last().append(templates[prefix].html());
          break;
        case "after":
        default:
          elements.last().after(templates[prefix].html());
          break;
      }
    }

    // Increment total forms in management form
    console.log("Total forms in formset '" + prefix + "': " + setTotal(++total) + ".");
    return true;
  }

  // Remove form from specified index (or closest containing form of button) of formset specified by prefix
  function removeForm(prefix, removedFormClass, kwargs) {
    // getTotal() returns undefined if prefix invalid
    var total = getTotal(prefix);
    if (total === undefined) {
      console.log("ERROR:\n\tNo formset exists with prefix '" + prefix + "'.");
      return false;
    }

    // Return if formset already has minimum number of forms
    // getMinNum() will not return undefined here, since addForm() returns earlier if prefix invalid
    if (total <= getMinNum(prefix)) {
      console.log("Minimum number of forms in formset '" + prefix + "' reached: " + total + ".");
      return false;
    }

    // Retrieve arguments
    var index = kwargs["index"];
    var button = kwargs["button"];

    // Find form to be removed
    var form;
    if (index === undefined) {
      // If index not defined, find closest containing form of button with specified prefix
      form = button.closest(formWrapperClass + "[" + formsetPrefixAttribute + "=\"" + prefix + "]");
      if (form === undefined) {
        // If not found, find closest containing form
        console.log("WARNING:\n\tNo containing elements with class '" + formWrapperClass + "' and attribute '" + formsetPrefixAttribute + "'.\n\tUsing only class instead.");
        form = button.closest(formWrapperClass);
      }
      if (form === undefined) {
        console.log("ERROR:\n\tNo containing elements with class '" + formWrapperClass + "'.");
        return false
      } else {
        // Get index of form
        index = parseFloat(form.find($("input[id^=\"id_" + prefix + "-\"").first()).attr("id").replace(RegExp("id_" + prefix + "-(\\d+)-.*"), "$1"));
        if (index === undefined) {
          // Since an invalid prefix would have been changed to the Django default "form", error caused by absence of input with Django generated id
          console.log("ERROR:/n/tForm contains no fields.");
          return false;
        }
      }
    } else {
      // If index defined, find all forms with specified prefix
      var forms = $(formWrapperClass + "[" + formsetPrefixAttribute + "=\"" + prefix + "]");
      if (forms === undefined) {
        // If not found, find all forms
        console.log("WARNING:\n\tNo elements with class '" + formWrapperClass + "' and attribute '" + formsetPrefixAttribute + "'.\n\tUsing only class instead.");
        forms = $(formWrapperClass);
      }
      if (forms === undefined) {
        console.log("ERROR:\n\tNo elements with class '" + formWrapperClass + "'.");
        return false
      } else {
        // Get form at specified index
        form = forms[index];
        if (form === undefined) {
          console.log("ERROR:\n\tInvalid index: " + index + ".");
          return false;
        }
      }
    }
    // Apply removed class to form or hide if class undefined
    if (removedFormClass === undefined) {
      form.css("display", "none");
    } else {
      form.attr("class", removedFormClass);
    }

    // Mark form for deletion with Django form deletion checkbox
    var name = prefix + "-" + index + "-DELETE";
    var id = "id_" + name;
    // Find checkbox or create if does not exist
    var deleteCheckbox = $("#" + id);
    if (deleteCheckbox === undefined) {
      // Add CSS to hide created checkbox
      deleteCheckbox = $("<input type=\"checkbox\">").attr({ "name": name, "id": id }).css("display", "none");
    }
    // Check checkbox and append to management form
    $("#id_" + prefix + "-MAX_NUM_FORMS").after(deleteCheckbox.prop("checked", true));

    // Return true for successful removal
    console.log("Marked form " + index + " of formset '" + prefix + "' for deletion.");
    return true;
  }


  // Event handlers

  $(buttonClass).click(function () {
    // The prefix of the formset to modify
    // Defaults to the Django default "form" if not set
    var prefix = $(this).attr(formsetPrefixAttribute);
    if (prefix === undefined) {
      console.log("WARNING:\n\tNo attribute '" + formsetPrefixAttribute + "' defined on this button.\n\tUsing Django default prefix 'form' instead.");
      prefix = "form";
    }

    // Whether button is always for adding forms
    // If not set, button is initially an add button and changes to a remove button on click
    // Set to true if attribute is set, false if not
    var addOnly = ($(this).attr(addOnlyAttribute) !== undefined) ? true : false;

    // Selector of element relative to which a new form will be inserted
    // Defaults to form wrapper class if not set
    var insertionSelector = $(this).attr(insertionSelectorAttribute);
    if (insertionSelector === undefined) {
      console.log("WARNING:\n\tNo attribute '" + insertionSelectorAttribute + "' defined on this button.\n\tUsing the form wrapper class '" + formWrapperClass + "' instead.");
      insertionSelector = formWrapperClass;
    }

    // Type of insertion as a string
    // addForm() handles undefined case
    var insertionType = $(this).attr(insertionTypeAttribute);

    // Whether button is for removing forms
    // Set to true if attribute is set, false if not
    var removeOnly = ($(this).attr(removeOnlyAttribute) !== undefined) ? true : false;

    // Index of form to remove
    // Defaults to last form with prefix if not set
    var value = $(this).attr(removalIndexAttribute);
    var removalIndex;
    if (value === undefined) {
      console.log("WARNING:\n\tNo attribute '" + removalIndexAttribute + "' defined on this button.\n\tRemoving closest containing form of formset '" + prefix + "' instead.");
    } else {
      removalIndex = parseInt(value);
      // removalIndex is NaN if value does not begin with numeric character.
      if (isNaN(removalIndex)) {
        console.log("ERROR:\n\tButton attribute '" + removalIndexAttribute + "' has invalid value: " + value + ".\n\tValue must be an integer.");
        return false;
      }
    }

    // Class to apply to removed forms
    // removeForm() handles undefined case
    var removedFormClass = $(this).attr(removedFormClassAttribute);

    // Manipulate formset
    if (removeOnly) {
      if (addOnly) {
        // Log error if both addOnly and removeOnly
        console.log("ERROR:\n\tButton has both attributes '" + addOnlyAttribute + "' and '" + removeOnlyAttribute + "'.\n\tOnly one of these attributes is permitted.");
        return false;
      } else {
        // Remove form
        console.log("Removing form " + removalIndex + "from formset '" + prefix + "'...");
        var kwargs = {
          "index": removalIndex,
          "button": $(this),
        }
        if (!removeForm(prefix, removedFormClass, kwargs)) {
          console.log("Failed to remove form from formset '" + prefix + "'.");
          return false;
        }
      }
    } else {
      // Add form
      console.log("Adding form to formset '" + prefix + "'...");
      if (!addForm(prefix, insertionSelector, insertionType)) {
        console.log("Failed to add form to formset '" + prefix + "'.");
        return false;
      }
      // Change to remove button if not addOnly
      if (!addOnly) {
        console.log("Adding attribute '" + removeOnlyAttribute + "' to button...");
        $(this).attr(removeOnlyAttribute, "");
      }
    }

    // Form management successful
    console.log("Operation completed.");
    return true;
  });
});
