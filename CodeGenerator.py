from ChatGPT import *
from Tooling.Tool import *

class Model:
    def __init__(self, sys_prompt, tools) -> None:
        if type(tools) != list:
            tools = [tools]

        self.sys_prompt = sys_prompt
        self.tools = tools
    
    def prompt(self, conv: list, ignore_response=False):
        conv.insert(len(conv) - 1, { "role": "system", "content": self.sys_prompt })

        return ChatGPT.smart_prompt(conv, self.tools, silent=True, ignore_response=ignore_response)

# Just an idea
# But is trying to make an AI for generating and modifing code and commenting on code 
class CodeGenerator:
    def gen_code():
        code = ""

    comment = None
    stop_commenting = False
    def add_code_comments(code: str):
        CodeGenerator.comment = None
        CodeGenerator.stop_commenting = False

        def add_comment(gpt_args):
            CodeGenerator.comment = gpt_args
        def stop_comment(gpt_args):
            CodeGenerator.stop_commenting = True

        comment_model = Model(
            # "You are given some code, and you add comments to explain the code by calling the add_comment tool, but only add comment if needed",
            "add comment only if the code need a comment added, otherwise call done. NEVER GIVE THE SAME COMMENT TWICE",
            [Tool(
                name="add_comment",
                description="This tool should be called if more comments should be added",
                args=[
                    ToolArg("comment_text", str).required(),
                    ToolArg("line_number", int).required().describe("The line in the code where the comment should be added"),
                    ToolArg("reason").required().describe("The reason for adding the comment")
                ],
                function_call=add_comment,
                default_response="Comment added to code"
            ),
            Tool(
                name="done",
                description="Call this tool when there is sufficiant comments",
                function_call=stop_comment,
                default_response="commenting stopped"
            )]
        )

        code_lines = code.split("\n")
        max_comments = 5 #AI KEPT MAKING THE SAME COMMENT?????
        comments_added = []
        while len(comments_added) < max_comments and not CodeGenerator.stop_commenting:
            CodeGenerator.comment = None

            code_prompt = [{"role":"user", "content": "\n\r".join(code_lines)}]
            comment_list_prompts = [{"role": "assistant", "content": "line added at " + str(a)} for a in comments_added]

            comment_model.prompt(comment_list_prompts + code_prompt, ignore_response=True)
            
            comment = CodeGenerator.comment

            if not comment:
                break

            line_number = comment["line_number"]
            text = comment["comment_text"]

            code_lines.insert(line_number - 1, "#" + text)
            # code_lines.insert(line_number, str(code_lines[line_number].count(" ") * " ") + "#" + text)


            print("Line " + str(line_number) + ": " + text)
            print("Reason:\n" + comment["reason"] + "\n")
            comments_added.append(line_number)

        
        return "\n".join(code_lines)


    
    evaluation = None
    def evaluate_code(code: str):
        def get_eval_back(gpt_args):
            CodeGenerator.evaluation = gpt_args

        evaluator_model = Model(
            "YOU MUST CALL THE EVALUATE TOOL." +
            "\nYou must comment on the code given, you return a short summary of what you think and call the evaluate tools."+
            "\nThe comment should not be much more than a few paragraphs",
            Tool(
                name="evaluate",
                args_description="All evaluations must be between 1 and 10",
                args=[
                    ToolArg("clean_eval", int).required().describe("How clean is the code"),
                    ToolArg("functional_eval", int).required().describe("How functional is the code"),
                ],
                function_call=get_eval_back,
                default_response="evaluation ratings given"
            )
        )

        response = evaluator_model.prompt([ {"role": "user", "content": code } ])

        print_info("Comment:\n" + response)
        print()
        print_warning("-Cleanliness:\n" + str(CodeGenerator.evaluation["clean_eval"]) + "/10")
        print_warning("-Functional:\n" + str(CodeGenerator.evaluation["functional_eval"]) + "/10")


if __name__ == "__main__":
    code = read_text_file("FileManager.py")

    # CodeGenerator.evaluate_code(code)
    print(CodeGenerator.add_code_comments(code))