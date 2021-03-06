import React from "react";
import { Button, Input } from "components";
import type { ValidationState } from "types";

type Props = {
  validationState: ValidationState,
  handleEnterKey: (SyntheticKeyboardEvent<HTMLInputElement>) => void,
  updateCurrentValue: string => void,
  handleSubmit: () => void
};

const Credentials = ({
  validationState,
  updateCurrentValue,
  handleEnterKey,
  handleSubmit
}: Props) => {
  const isSubmitDisabled = validationState !== "valid";
  return (
    <form>
      <Input
        label="ASUrite:"
        placeholder="Enter ASUrite"
        validationState={validationState}
        handleEnterKey={handleEnterKey}
        updateCurrentValue={updateCurrentValue}
        inputType="text"
      />
      <Button disabled={isSubmitDisabled} handleClick={handleSubmit}>
        {"Submit"}
      </Button>
    </form>
  );
};

export default Credentials;
