import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types.generative_service import GenerateContentResponse

class AssistantAI:
    def __init__(self, config):
        self.system_instruction = config.get("system_instruction", "")
        self.model_name = config.get("model_name", "")
        self.api_key = config.get("api_key", "")
        self.tools = config.get("tools", {})
        self.max_recursion = config.get("max_recursion", 5)
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=self.system_instruction,
            tools=self.tools
        )
    def generate_content(self, context):
        response = self.model.generate_content(contents=context, tools = self.tools)
        return response
        
    def parse_response(self, response:GenerateContentResponse):
        candidate = response.candidates[0].content.parts[0]
        if hasattr(candidate, 'function_call') and candidate.function_call.name != '':
            return {"type": "function_call", "name": candidate.function_call.name, "args": candidate.function_call.args}
        elif hasattr(candidate, 'text'):
            return {"type": "text", "text": candidate.text}
        else:
            return {"type": "unknown", "content": candidate}

    def get_tool_response(self, tool_name, args):
        tool = self.tools.get(tool_name, None)
        if tool is None:
            return {"message": "Tool not found.", "code":"TOOL_NOT_FOUND"}
        function = tool.get("function", None)
        if function is None:
            return {"message": "Function not found in tool.", "code":"FUNCTION_NOT_FOUND"}
        try:
            result = function(**args)
            return result
        except Exception as e:
            return {"message": str(e), "code":"FUNCTION_ERROR"}
    def interaction(self, context, count = 0):
        if not isinstance(context, list):
            raise ValueError("Le contexte doit être une liste.")
        if context[-1]["role"] not in [ "user", "function","system"]:
            raise ValueError("Le dernier rôle du contexte doit être 'user', 'function' ou 'system'.")
        out = self.generate_content(context)
        parsed_out = self.parse_response(out)
        if parsed_out["type"] == "function_call" and count < self.max_recursion:  # Limit recursion to prevent infinite loops
            tool_response = self.get_tool_response(parsed_out["name"], parsed_out["args"])
            context.append({
                "role": "function",
                "parts": [{
                    "function_response": {
                        "name": parsed_out["name"],
                        "response": tool_response
                    }
                }]
            })
            self.interaction(context, count+1)  # Recursive call to handle the function response
        elif parsed_out["type"] == "text":
            context.append({
                "role": "model",
                "parts": [{
                    "text": parsed_out["text"]
                }]
            })
            return context
