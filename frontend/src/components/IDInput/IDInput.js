// @flow
import React, { Component } from 'react';
import { Form, FormGroup, FormControl, ControlLabel, HelpBlock, Button, Tooltip } from 'react-bootstrap';

type Props = {
  onSubmit: (number) => void;
}

type State = {
  idValue: string,
  validID: boolean,
  acceptSubmit: boolean,
};

class IDInput extends Component<Props, State> {

  state = {
    idValue: '',
    validID: false,
    acceptSubmit: true,
  };

  getValidationState() {
    if (this.state.idValue.length <= 0) return null;
    else return this.state.validID ? 'success' :  'error';
  }

  isValidID = (input: string) => {
    const num = +input;  // parse to number; non-numeric answers will parse to NaN
    const isNumber = !isNaN(num);
    const length = num.toString().length;
    return length === 10 && isNumber;
  };

  handleIDInput = (e: SyntheticInputEvent<HTMLInputElement>) => {
    const input = e.currentTarget.value;
    this.setState({
      idValue: input,
      validID: this.isValidID(input),
    });
  };

  handleSubmit = () => {
    this.setState({
      acceptSubmit: this.state.validID
    });
    if (this.state.validID) {
      const parsedID = +this.state.idValue;
      this.props.onSubmit(parsedID);
    }
  };

  render() {
    return (
      <Form inline>
        <FormGroup
          controlId={"ID"}
          validationState={this.getValidationState()}
        >
          <ControlLabel>Student ID:</ControlLabel>
          {' '}
          <FormControl
            type={"text"}
            value={this.state.idValue}
            onChange={this.handleIDInput}
          />
          <FormControl.Feedback />
          <HelpBlock>Please enter a valid student ID.</HelpBlock>
        </FormGroup>
        <Button onClick={this.handleSubmit}>Submit</Button>  { /* typically has prop 'type="submit"', but reloads the page.. */ }
        { !this.state.acceptSubmit &&
          <Tooltip placement={"right"} className={"in"} id={"tooltip-right"}>Fix your ID before submitting!</Tooltip> }
      </Form>
    )
  }
}

export default IDInput;