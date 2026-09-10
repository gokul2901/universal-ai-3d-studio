import React, { useState, useRef, useEffect } from 'react';
import { Send, Sparkles, Mic, Loader2, Wand2 } from 'lucide-react';
import { useAIStore } from '../../store/useAIStore';
import { useSceneStore } from '../../store/useSceneStore';
import { useUIStore } from '../../store/useUIStore';
import { modify3DScene, explainTarget } from '../../services/api';
import { TTSPlayer } from '../voice/TTSPlayer';
import { VoiceRecorder } from '../voice/VoiceRecorder';
import { t } from '../../i18n';

export const AICopilot: React.FC = () => {
  const { messages, addMessage, isGenerating } = useAIStore();
  const { currentScene, selectedObjectId, setScene, setCameraMode, setExplodedProgress } = useSceneStore();
  const { language } = useUIStore();
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const quickPrompts = [
    t('chip_explain', language),
    t('chip_larger', language),
    t('chip_gold', language),
    t('chip_explode', language),
    t('chip_top_view', language),
    t('chip_explain_native', language)
  ];

  const handleSend = async (customText?: string) => {
    const textToSend = customText || inputText;
    if (!textToSend.trim() || !currentScene || isLoading) return;

    setInputText('');
    const userMsgId = `user_${Date.now()}`;
    addMessage({
      id: userMsgId,
      sender: 'user',
      text: textToSend,
      timestamp: new Date().toLocaleTimeString(),
    });

    setIsLoading(true);

    try {
      const lower = textToSend.toLowerCase();

      // Check quick client-side camera/view commands
      if (lower.includes('top view')) {
        setCameraMode('top');
      } else if (lower.includes('front view')) {
        setCameraMode('front');
      } else if (lower.includes('isometric')) {
        setCameraMode('isometric');
      } else if (lower.includes('explode')) {
        setExplodedProgress(1.0);
      } else if (lower.includes('assemble') || lower.includes('reset view')) {
        setExplodedProgress(0.0);
      }

      // Check if user is asking for an explanation across languages
      const isExplain =
        lower.includes('explain') ||
        lower.includes('what is') ||
        lower.includes('விளக்கு') ||
        lower.includes('समझाओ') ||
        lower.includes('বিবরণ') ||
        lower.includes('వివరించు') ||
        lower.includes('स्पष्टीकरण') ||
        lower.includes('വിശദീകരിക്കുക') ||
        lower.includes('وضاحت') ||
        lower.includes('explica') ||
        lower.includes('détaille') ||
        lower.includes('beschreibe') ||
        lower.includes('объясни') ||
        lower.includes('解析') ||
        lower.includes('解説') ||
        textToSend === t('chip_explain', language) ||
        textToSend === t('chip_explain_native', language);

      if (isExplain) {
        const selectedObj = currentScene.objects.find(o => o.id === selectedObjectId) || currentScene.objects[0];
        let targetLang = language;
        if (lower.includes('tamil')) targetLang = 'ta';
        else if (lower.includes('hindi')) targetLang = 'hi';
        else if (lower.includes('spanish')) targetLang = 'es';
        else if (lower.includes('arabic')) targetLang = 'ar';
        
        const explainRes = await explainTarget({
          target_name: selectedObj ? selectedObj.name : currentScene.title,
          category: selectedObj ? selectedObj.category : 'scene',
          language: targetLang,
          context: {
            scene: currentScene.title,
            components: selectedObj?.components?.map(c => c.name)
          }
        });

        addMessage({
          id: `ai_${Date.now()}`,
          sender: 'ai',
          text: `### ${explainRes.title}\n\n${explainRes.explanation}\n\n**${t('purpose_and_analysis', targetLang)}:** ${explainRes.purpose}`,
          language: explainRes.language || targetLang,
          timestamp: new Date().toLocaleTimeString(),
          target_id: selectedObj?.id
        });
      } else {
        // Execute natural language scene modification with target language
        const res = await modify3DScene({
          project_id: currentScene.id,
          instruction: textToSend,
          language: language,
          current_scene: currentScene,
          selected_object_id: selectedObjectId
        });

        if (res.success && res.scene) {
          setScene(res.scene);
          addMessage({
            id: `ai_${Date.now()}`,
            sender: 'ai',
            text: res.explanation || `Applied modification: "${textToSend}"`,
            language: language,
            timestamp: new Date().toLocaleTimeString()
          });
        }
      }
    } catch (err: any) {
      addMessage({
        id: `err_${Date.now()}`,
        sender: 'ai',
        text: `We couldn't modify this scene yet. Try simplifying the command or selecting an object.`,
        timestamp: new Date().toLocaleTimeString()
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-dark-900/40 text-xs">
      {/* Header */}
      <div className="flex items-center justify-between p-3.5 border-b border-white/10 bg-dark-950/60 backdrop-blur-md">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 rounded-lg bg-gradient-to-tr from-primary-500 to-accent-cyan flex items-center justify-center shadow-md">
            <Sparkles className="w-3.5 h-3.5 text-white" />
          </div>
          <div>
            <h3 className="font-display font-semibold text-white tracking-wide">
              {t('copilot_title', language)}
            </h3>
            <p className="text-[10px] text-slate-400">{t('copilot_subtitle', language)}</p>
          </div>
        </div>
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3.5">
        {messages.map((msg) => {
          const displayText = msg.id === 'welcome' ? t('welcome_copilot', language) : msg.text;
          return (
            <div
              key={msg.id}
              className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}
            >
              <div
                className={`max-w-[88%] p-3 rounded-2xl select-text leading-relaxed ${
                  msg.sender === 'user'
                    ? 'bg-gradient-to-r from-primary-600 to-indigo-600 text-white rounded-br-none shadow-md'
                    : 'glass-panel border border-white/10 text-slate-200 rounded-bl-none shadow-sm'
                }`}
              >
                <div className="whitespace-pre-wrap">{displayText}</div>

                {/* TTS Audio Player on AI responses */}
                {msg.sender === 'ai' && (
                  <div className="mt-2.5 pt-2 border-t border-white/10">
                    <TTSPlayer text={displayText.replace(/[#*]/g, '')} language={msg.language || language} />
                  </div>
                )}
              </div>
              <span className="text-[9px] text-slate-500 mt-1 px-1">{msg.timestamp}</span>
            </div>
          );
        })}
        {isLoading && (
          <div className="flex items-center gap-2 p-3 glass-panel rounded-2xl rounded-bl-none text-slate-400 w-fit">
            <Loader2 className="w-3.5 h-3.5 animate-spin text-primary-400" />
            <span className="text-[11px]">{t('thinking_modifying', language)}</span>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      {/* Suggested Quick Prompts */}
      <div className="px-3 py-2 border-t border-white/5 flex gap-1.5 overflow-x-auto no-scrollbar">
        {quickPrompts.map((qp, i) => (
          <button
            key={i}
            onClick={() => handleSend(qp)}
            className="whitespace-nowrap px-2.5 py-1 rounded-full text-[10px] font-medium bg-white/5 hover:bg-primary-500/20 text-slate-300 hover:text-primary-300 border border-white/5 transition-colors shrink-0"
          >
            {qp}
          </button>
        ))}
      </div>

      {/* Input Composer */}
      <div className="p-3 border-t border-white/10 bg-dark-950/80 backdrop-blur-md flex items-center gap-2">
        <VoiceRecorder
          onTranscriptionComplete={(text) => handleSend(text)}
          languageHint={language}
        />
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder={t('copilot_input_placeholder', language)}
          className="flex-1 bg-dark-900 border border-white/10 rounded-xl px-3 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-primary-500/60 transition-colors"
        />
        <button
          type="button"
          onClick={() => handleSend()}
          disabled={!inputText.trim() || isLoading}
          className="p-2.5 rounded-xl bg-primary-500 hover:bg-primary-600 disabled:opacity-40 text-white shadow-lg shadow-primary-500/20 transition-all"
        >
          <Send className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
};
