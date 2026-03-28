class OpenAIProvider:
    async def chat_tutor(self, message, context):
        raise NotImplementedError("OpenAI provider not configured")

    async def generate_practice(self, module_id, difficulty=None):
        raise NotImplementedError("OpenAI provider not configured")

    async def assess_practice(self, prompt, answer, context):
        raise NotImplementedError("OpenAI provider not configured")

    async def explain_concept(self, concept, level=None, context=None):
        raise NotImplementedError("OpenAI provider not configured")
