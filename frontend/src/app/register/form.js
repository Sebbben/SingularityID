"use client";
import { makeParamsString } from "@/utils/general";
import { Form, Input, Checkbox, Button, Link } from "@nextui-org/react";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function RegisterForm({ params }) {
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState(""); // New state for confirm password
  const [errors, setErrors] = useState({});
  const router = useRouter();

  // Real-time password validation
  const getPasswordError = (value) => {
    // A strong password:
    // - At least 9 characters
    // - Contains uppercase and lowercase letters
    // - Contains digits
    // - Contains special characters
    if (value == "") return null;
    if (value.length < 9) {
      return "Password must be 9 characters or more";
    }
    if ((value.match(/[A-Z]/g) || []).length < 1) {
      return "Password needs at least 1 uppercase letter";
    }
    if ((value.match(/[a-z]/g) || []).length < 1) {
      return "Password needs at least 1 lowercase letter";
    }
    if ((value.match(/[0-9]/g) || []).length < 1) {
      return "Password needs at least 1 digit";
    }
    if ((value.match(/[!@#$%^&*(),.?\":{}|<>]/g) || []).length < 1) {
      return "Password needs at least 1 special character";
    }

    return null;
  };

  // New function to check if passwords match
  const getConfirmPasswordError = (value) => {
    if (value !== password) {
      return "Passwords do not match";
    }
    return null;
  };

  const onSubmit = (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.currentTarget));

    // Custom validation checks
    const newErrors = {};

    // Password validation
    const passwordError = getPasswordError(data.password);
    const confirmPasswordError = getConfirmPasswordError(data.confirmPassword); // Check confirm password

    if (passwordError) {
      newErrors.password = passwordError;
    }

    if (confirmPasswordError) {
      newErrors.confirmPassword = confirmPasswordError;
    }

    // Username validation
    if (data.username === "admin") {
      newErrors.username = "Nice try! Choose a different username";
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    if (data.terms !== "true") {
      setErrors({ terms: "Please accept the terms" });
      return;
    }

    // Clear errors and submit
    setErrors({});

    const registerFormData = {
      username: data.username,
      password: data.password,
      confirm_password: data.confirmPassword,
      terms: data.terms,
      client_id: params.client_id,
      response_type: params.response_type,
      redirect_uri: params.redirect_uri,
      state: params.state
    };


    // Submit data to api endpoint
    fetch("/api/auth/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(registerFormData),
    })
      .then((res) => {
        return res.json()
      })
      .then((res) => {
        if (res.error) {
          console.error(res.error);
        } else {
          if (res.redirect_uri) {
            router.push(res.redirect_uri)
          }
        }
      })
      .catch((err) => console.error);
  };

  const handleRedirectLogin = (e) => {
    e.preventDefault(true);
    router.push("/login?"+makeParamsString(params))
  };

  return (
    <Form
      className="w-full justify-center items-center space-y-4"
      validationBehavior="native"
      validationErrors={errors}
      onSubmit={onSubmit}
    >
      <div className="flex flex-col gap-4 max-w-md">
        <Input
          isRequired
          errorMessage={({ validationDetails }) => {
            if (validationDetails.valueMissing) {
              return "Please enter your username";
            }
            return errors.username;
          }}
          label="Username"
          labelPlacement="outside"
          name="username"
          placeholder="Enter your username"
        />

        <Input
          isRequired
          errorMessage={getPasswordError(password)}
          isInvalid={getPasswordError(password) !== null}
          label="Password"
          labelPlacement="outside"
          name="password"
          placeholder="Enter your password"
          type="password"
          value={password}
          onValueChange={setPassword}
        />

        <Input
          isRequired
          errorMessage={getConfirmPasswordError(confirmPassword)}
          isInvalid={getConfirmPasswordError(confirmPassword) !== null}
          label="Confirm Password"
          labelPlacement="outside"
          name="confirmPassword"
          placeholder="Confirm your password"
          type="password"
          value={confirmPassword}
          onValueChange={setConfirmPassword}
        />

        <Checkbox
          isRequired
          classNames={{
            label: "text-small",
          }}
          isInvalid={!!errors.terms}
          name="terms"
          validationBehavior="aria"
          value="true"
          onValueChange={() =>
            setErrors((prev) => ({ ...prev, terms: undefined }))
          }
        >
          I agree to the terms and conditions
        </Checkbox>

        {errors.terms && (
          <span className="text-danger text-small">{errors.terms}</span>
        )}

        <div className="flex gap-4">
          <Button className="w-full" color="primary" type="submit">
            Register
          </Button>
          <Button type="reset" variant="bordered">
            Reset
          </Button>
        </div>
        <div className="flex justify-center align-items-center text-sm">
          <p className="flex items-center">
            Already have an account? &nbsp;
            <Link className="text-small" href="/login" onClick={handleRedirectLogin}>
              Login here
            </Link>
          </p>
        </div>
      </div>
    </Form>
  );
}
