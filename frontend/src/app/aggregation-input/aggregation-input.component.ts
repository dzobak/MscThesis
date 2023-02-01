import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-aggregation-input',
  templateUrl: './aggregation-input.component.html',
  styleUrls: ['./aggregation-input.component.css'],
  inputs: ['columnsToDisplay', 'rule']
})
export class AggregationInputComponent {
  @Output() inputChange: EventEmitter<numeric_input> = new EventEmitter<numeric_input>();
  @Output() ruleDeleted: EventEmitter<string> = new EventEmitter<string>();


  columnsToDisplay!: string[];
  isit = true
  value = ''

  operators = [
    '\u{2264}', //less or equal
    '\u{2264}', //greater or equal
    '=',
    '<',
    '>',
  ]

  rule: numeric_input = {
    attribute: '',
    bool: true,
    operator: '',
    compared: '',
    value: ''
  };

  constructor() { }

  changedInput() {
    console.log(this.rule)
    this.inputChange.emit(this.rule)
    console.log(this.rule)
  }

  deleteRule() {
    this.ruleDeleted.emit()
  }
}


export interface numeric_input {
  attribute: string,
  bool: boolean,
  operator: string,
  compared: string,
  value: string
}

