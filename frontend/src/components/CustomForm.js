import React from "react";
import { Input, Button, Checkbox, Form, Link } from "@nextui-org/react";

/**
 * CustomForm component to create reusable forms.
 * 
 * @param {Array} fields - Array of field objects to render in the form.
    * @param {Boolean} fields[].isRequired - Indicates if the field is required.
    * @param {String} fields[].errorMessage - Error message for the field.
    * @param {Boolean} fields[].isInvalid - Indicates if the field is invalid.
    * @param {String} fields[].label - Label for the field.
    * @param {String} fields[].labelPlacement - Placement of the label.
    * @param {String} fields[].name - Name of the field.
    * @param {String} fields[].placeholder - Placeholder text for the field.
    * @param {String} fields[].type - Type of the field (e.g., text, checkbox).
    * @param {String} fields[].value - Value of the field.
    * @param {Function} fields[].onValueChange - Function to handle value change of the field.
 * @param {Function} onSubmit - Function to handle form submission.
 * @param {Function} onReset - Function to handle form reset.
 * @param {String} submitButtonText - Text for the submit button.
 * @param {String} resetButtonText - Text for the reset button.
 * @param {String} linkText - Text for the optional link.
 * @param {String} linkHref - Href for the optional link.
 * @param {Function} linkOnClick - Function to handle click on the optional link.
 * @param {Object} errors - Object containing validation errors.
 * @param {String} errors.terms - Validation error message for terms and conditions.
 */
export const CustomForm = ({ fields, onSubmit, onReset, submitButtonText, resetButtonText, linkText, linkHref, linkOnClick, errors }) => {
    return (
        <Form
            className="w-full justify-center items-center space-y-4"
            validationBehavior="native"
            validationErrors={errors}
            onSubmit={onSubmit}
        >
            <div className="flex flex-col gap-4 max-w-md">
                {fields.map((field, index) => (
                    <Input
                        key={index}
                        isRequired={field.isRequired}
                        errorMessage={field.errorMessage}
                        isInvalid={field.isInvalid}
                        label={field.label}
                        labelPlacement="outside"
                        name={field.name}
                        placeholder={field.placeholder}
                        type={field.type}
                        value={field.value}
                        onValueChange={field.onValueChange}
                        fullWidth
                    />
                ))}
                {fields.some(field => field.type === "checkbox") && (
                    <Checkbox
                        isRequired={fields.find(field => field.type === "checkbox").isRequired}
                        classNames={{ label: "text-small" }}
                        isInvalid={!!errors.terms}
                        name="terms"
                        validationBehavior="aria"
                        value="true"
                        onValueChange={() => setErrors((prev) => ({ ...prev, terms: undefined }))}
                    >
                        I agree to the terms and conditions
                    </Checkbox>
                )}
                {errors.terms && (
                    <span className="text-danger text-small">{errors.terms}</span>
                )}
                <div className="flex gap-4">
                    <Button className="w-full" color="primary" type="submit">
                        {submitButtonText}
                    </Button>
                    <Button type="reset" variant="bordered" onClick={onReset}>
                        {resetButtonText}
                    </Button>
                </div>
                {linkText && (
                    <div className="flex justify-center align-items-center text-sm">
                        <p className="flex items-center">
                            {linkText} &nbsp;
                            <Link className="text-small" href={linkHref} onClick={linkOnClick}>
                                {linkText}
                            </Link>
                        </p>
                    </div>
                )}
            </div>
        </Form>
    );
};

