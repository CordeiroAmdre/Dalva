import { SendOutlined } from "@ant-design/icons";
import ReactECharts from "echarts-for-react";
import { useMemo, useState } from "react";
import {
  Alert,
  Button,
  Card,
  Input,
  Layout,
  List,
  Space,
  Spin,
  Tag,
  Typography,
} from "antd";

import { useChatSession } from "../hooks/useChatSession";
import type { AssistantChatMessage, ChatThreadItem } from "../types/chat";
import { MESSAGE_MAX_LENGTH, isRenderableChart } from "../types/chat";

const { Content, Footer } = Layout;
const { Text, Paragraph, Title } = Typography;
const { TextArea } = Input;

function renderAssistantMeta(message: AssistantChatMessage) {
  return (
    <Space wrap size={[4, 4]} style={{ marginTop: 8 }}>
      {message.usedDatabase ? (
        <Tag color="green">Dados do PDV</Tag>
      ) : (
        <Tag>Resposta geral</Tag>
      )}
      {message.dataSources.map((source) => (
        <Tag key={source} color="blue">
          {source}
        </Tag>
      ))}
      <Text type="secondary" style={{ fontSize: 12 }}>
        {message.model}
      </Text>
    </Space>
  );
}

function renderMessage(item: ChatThreadItem) {
  if (item.kind === "user") {
    return (
      <List.Item>
        <Card size="small" style={{ width: "100%", background: "#e6f4ff" }}>
          <Text strong>Você</Text>
          <Paragraph style={{ marginBottom: 0, whiteSpace: "pre-wrap" }}>
            {item.text}
          </Paragraph>
        </Card>
      </List.Item>
    );
  }

  return (
    <List.Item>
      <Card size="small" style={{ width: "100%" }}>
        <Text strong>Dalva</Text>
        <Paragraph style={{ whiteSpace: "pre-wrap" }}>{item.reply}</Paragraph>
        {renderAssistantMeta(item)}
        {isRenderableChart(item.chart) ? (
          <div style={{ marginTop: 16, height: 360, width: "100%" }}>
            <ReactECharts
              key={item.id}
              option={item.chart.option}
              style={{ height: "100%", width: "100%" }}
              opts={{ renderer: "canvas" }}
              notMerge
              lazyUpdate
            />
          </div>
        ) : null}
      </Card>
    </List.Item>
  );
}

export default function ChatPage() {
  const { messages, isLoading, error, inputError, sendMessage } = useChatSession();
  const [draft, setDraft] = useState("");

  const remainingChars = useMemo(
    () => MESSAGE_MAX_LENGTH - draft.length,
    [draft.length],
  );

  const handleSend = async () => {
    const currentDraft = draft;
    setDraft("");
    await sendMessage(currentDraft);
  };

  return (
    <Layout style={{ minHeight: "100vh", maxWidth: 960, margin: "0 auto" }}>
      <Content style={{ padding: "24px 24px 0" }}>
        <Title level={3} style={{ marginTop: 0 }}>
          Dalva — Chat com seus dados
        </Title>
        <Text type="secondary">
          Faça perguntas sobre produtos, vendas, lojas e pagamentos em linguagem natural.
        </Text>

        {error ? (
          <Alert
            type="error"
            showIcon
            message={error.message}
            style={{ marginTop: 16 }}
          />
        ) : null}

        <List
          style={{ marginTop: 16, minHeight: 320 }}
          dataSource={messages}
          renderItem={renderMessage}
          locale={{ emptyText: "Envie uma pergunta para iniciar a conversa." }}
        />

        {isLoading ? (
          <div style={{ textAlign: "center", padding: 16 }}>
            <Spin tip="Consultando dados..." />
          </div>
        ) : null}
      </Content>

      <Footer style={{ background: "#fff", borderTop: "1px solid #f0f0f0" }}>
        <Space direction="vertical" style={{ width: "100%" }} size="small">
          <TextArea
            value={draft}
            onChange={(event) => setDraft(event.target.value)}
            placeholder="Ex.: Qual foi o valor total de vendas ontem?"
            aria-label="Mensagem do chat"
            autoSize={{ minRows: 2, maxRows: 6 }}
            maxLength={MESSAGE_MAX_LENGTH}
            disabled={isLoading}
            onPressEnter={(event) => {
              if (!event.shiftKey) {
                event.preventDefault();
                void handleSend();
              }
            }}
          />
          <Space style={{ width: "100%", justifyContent: "space-between" }}>
            <Text type={inputError ? "danger" : "secondary"}>
              {inputError ?? `${remainingChars} caracteres restantes`}
            </Text>
            <Button
              type="primary"
              icon={<SendOutlined />}
              loading={isLoading}
              aria-label="Enviar mensagem"
              onClick={() => void handleSend()}
            >
              Enviar
            </Button>
          </Space>
        </Space>
      </Footer>
    </Layout>
  );
}
