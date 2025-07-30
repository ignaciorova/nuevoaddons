{
    'name': 'AI Automation Base',
    'version': '1.0.0',
    'category': 'Extra Tools/AI',
    'summary': 'Base module for integrating major LLM providers into Odoo',
    'description': """
        AI Automation Base is a comprehensive, enterprise-grade Odoo module that provides a secure, 
        scalable, and extensible foundation for integrating Large Language Models (LLMs) into your Odoo ecosystem. 
        Built with modern architecture and security best practices, it enables seamless AI automation 
        across all your business processes.
        
        Key Features:
        - Secure API key management with encryption
        - Provider-agnostic interface for OpenAI, Google Gemini, and Anthropic Claude
        - Text generation, chat completion, and embeddings support
        - Streaming responses and function calling capabilities
        - Comprehensive monitoring and analytics
        - Modern, responsive user interface
        - Enterprise-grade security and access control
        
        Transform your Odoo with the power of AI automation!
    """,
    'author': 'ECOSIRE (PRIVATE) LIMITED',
    'website': 'https://www.ecosire.com',
    'email': 'info@ecosire.com',
    'depends': ['base', 'web'],
    'data': [
        'security/ai_automation_base_security.xml',
        'security/ir.model.access.csv',
        'views/ai_automation_base_menus.xml',
        'views/llm_provider_views.xml',
        'views/llm_api_key_views.xml',
        'views/llm_provider_model_views.xml',
        'views/llm_request_log_views.xml',
        'data/default_providers.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'images': [
        'static/description/cover.png',
        'static/description/icon.png',
        'static/description/icons/icon_16.png',
        'static/description/icons/icon_32.png',
        'static/description/icons/icon_64.png',
        'static/description/icons/icon_128.png',
        'static/description/icons/icon_256.png',
        'static/description/main_screenshot.png',
        'static/description/provider_configuration.png',
        'static/description/ai_dashboard.png',
        'static/description/usage_analytics.png',
    ],
    'price': 0.0,
    'currency': 'USD',
    'support': 'info@ecosire.com',
    'maintainer': 'ECOSIRE (PRIVATE) LIMITED',
    'contributors': [],
    'external_dependencies': {
        'python': ['requests', 'json', 'cryptography'],
    },
    'assets': {
        'web.assets_backend': [
            'ai_automation_base/static/src/js/llm_service.js',
            'ai_automation_base/static/src/css/llm_interface.css',
        ],
    },
} 