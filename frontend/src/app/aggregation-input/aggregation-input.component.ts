import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-aggregation-input',
  templateUrl: './aggregation-input.component.html',
  styleUrls: ['./aggregation-input.component.css'],
  inputs: ['columnsToDisplay', 'rule']
})
export class AggregationInputComponent {
  @Output() inputChange: EventEmitter<aggregation_rule> = new EventEmitter<aggregation_rule>();
  @Output() ruleDeleted: EventEmitter<string> = new EventEmitter<string>();


  columnsToDisplay!: string[];
  isit = true
  value = ''

  operators = [
    '\u{2264}', //less or equal
    '\u{2265}', //greater or equal
    '=',
    '<',
    '>',
  ]

  rule: aggregation_rule | numeric_rule = {
    attribute: '',
    bool: "",
    operator: '',
    // compared: '',
    value: ''
  };



  constructor() { }

  changedInput() {
    this.inputChange.emit(this.rule)
  }

  deleteRule() {
    this.ruleDeleted.emit()
  }
}


export interface aggregation_rule {
  attribute: string,
  level?: number,
  bool: string,
  operator: string,
  compared?: string,
  n?: number,
  value: string,
  unified?: string
}

export interface numeric_rule extends aggregation_rule{
  attribute: string,
  bool: string,
  operator: string,
  compared: string,
  value: string
}

