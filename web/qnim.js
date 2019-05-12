let gameSize = 10;
let actionSpace = [1, 2, 3];

function getSum(total, num){
    return total + num;
}

let game = new Object();
game.sticks = gameSize;
game.remove = function(count) {
    game.sticks -= count;
};
game.getState = function() {
    return game.sticks - 1;
};
game.isOver = function() {
    return game.sticks <= 0;
};
game.reset = function() {
    game.sticks = gameSize;
};

let qlearner = new Object();
qlearner.q = [];
for (i = 0; i < gameSize; i++) {
    stateQ = []
    for (j = 0; j < actionSpace.length; j++) {
        stateQ.push(0);
    }
    qlearner.q.push(stateQ);
};
qlearner.getMove = function(state) {
    potentialActions = qlearner.q[state];
    maxActionIndex = potentialActions.indexOf(Math.max(potentialActions));
    return actionSpace[maxActionIndex];
};
qlearner.learn = function(state, action, new_state, reward, is_over) {
    if (is_over) {
        qlearner.q[state][action] = reward
    } else {
        qlearner.q[state][action] = reward + (qlearner.q[new_state].reduce(getSum) / actionSpace.length);
    }
};

function say(outputString) {
    document.getElementById("output").innerHTML = outputString;
}

state = game.getState();

function takeTurn(sticksToRemove) {
    
}

function takeOneStick() {
    takeTurn(1);
}

function takeTwoSticks() {
    takeTurn(2);
}

function takeThreeSticks() {
    takeTurn(3);
}
