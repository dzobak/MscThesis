import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-aggregation-input',
  templateUrl: './aggregation-input.component.html',
  styleUrls: ['./aggregation-input.component.css'],
  inputs: ['columnsToDisplay', 'rule', 'columnTypes']
})
export class AggregationInputComponent {
  @Output() inputChange: EventEmitter<aggregation_rule> = new EventEmitter<aggregation_rule>();
  @Output() ruleDeleted: EventEmitter<string> = new EventEmitter<string>();


  columnsToDisplay!: string[];
  columnTypes!: { [Key: string]: any }
  isit = true
  value = ''


  num_operators = [
    '\u{2264}', //less or equal
    '\u{2265}', //greater or equal
    '=',
    '<',
    '>',
  ]

  cat_operators =[
    
    '='
  ]

  rule: aggregation_rule = {
    attribute: '',
    bool: "",
    operator: '',
    // compared: '',
    value: ''
  };



  constructor() { }

  changedAttribute() {
    console.log(this.columnTypes[this.rule.attribute])
    this.rule.type = this.columnTypes[this.rule.attribute]
    this.changedInput()
  }

  changedInput() {
    console.log((this.rule.type == 'categorical' || this.rule.type == 'scope'))
    console.log(this.rule.value == 'last' || this.rule.value=='first')
    console.log(this.rule.value)
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
  unified?: string,
  type?: string
}

// export interface numeric_rule extends aggregation_rule{
//   attribute: string,
//   bool: string,
//   operator: string,
//   compared: string,
//   value: string
// }

// export interface scope_rule extends aggregation_rule{
//   attribute: string,
//   level: number,
//   bool: string,
//   operator: string,
//   compared?: string,
//   n?: number,
//   value: string,
//   unified?: string
// }

