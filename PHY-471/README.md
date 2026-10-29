# Using BraKetApp

## Running the file

To run the file, one should 'open with Python' the file, `BraKetApp.py`.
Alternatively, one can run the file with a terminal, by navigating to the directory containing `BraKetApp.py` by executing the command, `python -m BraKetApp`.

## Using the app

Once the file executes, a GUI will appear that will show many different textboxes and buttons.
Most of them are self-explanatory, but a few are a little odd.
All quantum states should be presented as `a|a_1> + b|a_2> -c|b_1>`, where `a,b,c` are all coefficients of the kets they are next to, and `|a_1>, |a_2>, |b_1>` are all kets, indexed by `a_1,a_2,b_1` respectively. There is no limit on the number of kets in an expression.
A user should, before utilizing any calculation feature, first initialize any expressions that they wish to see calculated as variables, by inputting them in the first box, and pressing the `Initialize` button. Then, they should indicate which indices will denote orthonormal bases in the bottom entry box, in the form of `{a_1,a_2,a_3},{b_1,b_2}`.
Then, a user can input their ket to be evaluated, and press other buttons.
The `|phi>` entry denotes a separate ket to be sandwiched with `|psi>`.