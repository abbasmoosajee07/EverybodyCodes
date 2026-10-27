import { TuringConfig } from './TuringBrain.js';
import { MachineLogic } from './TuringBrain.js';

class TuringMachine {
    constructor(transitionsStr, maxSteps = 1_000_000) {
        this.MAX_STEPS = maxSteps;
        this.transitionsStr = transitionsStr;
        const transitions = new TuringConfig().parseTransitionRules(this.transitionsStr);
        this.cpu = new MachineLogic(transitions);
    }

    load_tape() {
        this.cpu._setTape(this.initialTape);
        this.init_time = TuringConfig.getTimestamp();
        this.step_count = 0;
    }

    printSummary() {
        const final_tape = this.cpu._printTapeState(false);
        const run_time = (TuringConfig.getTimestamp() - this.init_time).toFixed(3);
        console.log("=== RUN COMPLETE ===");
        console.log(`Final Tape: ${final_tape}`);
        console.log(`Steps: ${this.step_count}`);
        console.log(`Rules: ${this.cpu.transitions_list.length}`);
        console.log(`Time Elapsed: ${run_time}s`);
        console.log(`Memory Used: ${TuringConfig.getCurrentMemoryMB()} MB`);
    }

    async run_machine(initialTape, play_type = 0, visualize = false) {
        this.initialTape = initialTape;
        this.load_tape();

        let result;
        if (play_type === 0) {
            result = this.cpu.runLogic(initialTape, this.MAX_STEPS, visualize);
        } else if (play_type === 1) {
            result = await this.cpu.runIncrementally(initialTape, visualize, this.MAX_STEPS);
        }

        if (result) {
            const [, steps] = result;
            this.step_count = steps;
        }

        if (visualize) {
            this.printSummary();
        };
    }
}

export { TuringMachine }
