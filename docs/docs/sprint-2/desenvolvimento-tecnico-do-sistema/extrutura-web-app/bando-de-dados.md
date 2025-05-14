---
sidebar_position: 1
custom_edit_url: null
---

# Banco de dados

## Introdução

O banco de dados representa um componente essencial para o Sistema Óptico de Detecção (SOD), fornecendo a infraestrutura de armazenamento necessária para todas as operações do sistema. Para um projeto de análise e detecção de fissuras em edificações utilizando drones, a estrutura de dados deve suportar não apenas o armazenamento das imagens capturadas, mas também os resultados das análises realizadas pela inteligência artificial, informações sobre os projetos, usuários e relatórios gerados.

O SOD captura imagens de fachadas de edifícios através de drones, processa essas imagens com modelos de IA para detectar, classificar e avaliar a gravidade de fissuras, e finalmente gera relatórios técnicos detalhados. Um banco de dados bem estruturado é importante para garantir a rastreabilidade dos dados, o histórico de inspeções, e a confiabilidade das análises ao longo do tempo.

## Estrutura do Banco de Dados

O banco de dados foi implementado utilizando o Supabase, uma plataforma de desenvolvimento que oferece funcionalidades de banco de dados PostgreSQL com APIs. A estrutura foi projetada para atender às necessidades específicas das personas de Mariana Ribeiro (Pesquisadora) e Carlos Eduardo (Técnico de Edificações), garantindo tanto o rigor técnico-científico quanto a praticidade operacional.

### Diagrama do Esquema de Dados

O esquema do banco de dados é composto por oito tabelas principais, organizadas para suportar as funcionalidades essenciais do sistema:

# Database Schema for Crack Analysis System

```sql
# User Management
users: {
  shape: sql_table
  id: uuid {constraint: primary_key}
  name: text
  email: text
  role: text
  created_at: timestamp with time zone
  updated_at: timestamp with time zone
  last_login: timestamp with time zone
}

# Project Management
projects: {
  shape: sql_table
  id: serial {constraint: primary_key}
  name: text
  description: text
  address: text
  created_at: timestamp with time zone
  updated_at: timestamp with time zone
}

# User-Project Association
user_projects: {
  shape: sql_table
  id: serial {constraint: primary_key}
  user_id: uuid {constraint: foreign_key}
  project_id: integer {constraint: foreign_key}
}

# Image Management
images: {
  shape: sql_table
  id: serial {constraint: primary_key}
  user_id: uuid {constraint: foreign_key}
  project_id: integer {constraint: foreign_key}
  file_path: text
  file_name: text
  type: text
  size_kb: integer
  axis: text
  floor: text
  uploaded_at: timestamp with time zone
  metadata: jsonb
}

# Analysis Results
results: {
  shape: sql_table
  id: serial {constraint: primary_key}
  user_id: uuid {constraint: foreign_key}
  trustability: integer
  severity: integer
  type: text
  created_at: timestamp with time zone
}

# Project-Results Association
project_results: {
  shape: sql_table
  id: serial {constraint: primary_key}
  result_id: integer {constraint: foreign_key}
  project_id: integer {constraint: foreign_key}
}

# Reports
reports: {
  shape: sql_table
  id: serial {constraint: primary_key}
  user_id: uuid {constraint: foreign_key}
  project_id: integer {constraint: foreign_key}
  result_id: integer {constraint: foreign_key}
  file_path: text
  generated_at: timestamp with time zone
}

# Report-Image Association
reports_images: {
  shape: sql_table
  id: serial {constraint: primary_key}
  report_id: integer {constraint: foreign_key}
  image_id: integer {constraint: foreign_key}
}
```

<p style={{textAlign: 'center'}}>Figura 1: Estrutura do banco de dados</p>
<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
        <img src={require("../../../../static/img/database/database.png").default} style={{width: 800}} alt="Tela de login" />
        <br />
    </div>
</div>
<p style={{textAlign: 'center'}}>Fonte: Produzida pelos Autores (2025). </p>

[Link para o D2 para melhor visualização](https://play.d2lang.com/?script=zFbBbtswDL3rKwj0nB_wYUC3XXYYMLTY2WBsxmEjS55Ib3WL_PtgKVacpsjcIRt6MkTSJB_fo-wb-IyKaxSC-2pLLcLGB_gUsNrBrUM7CAvcD6LUGnMD34UCfEWHDbXk1PRCQQp4NgCyxY4KkB-2VFxbMgBcF9D3XMNz5Z1oQHZaQBe4xTCUOxr2BsBhSwUoPaoBoBbZ5lPw9uiqAqFSXaIWoNySKLYd_GLdxiM8eTfW7Lt6SZhF0dL6ht2FsP0I-VvwD1TpHHWXTJeBCwVGuxx6TVIF7pS9yzas60Ai_2QG-4nP1YTwVsRXjGMHkdjyWjhjstfFsPGBuHFT5KFiDGan1FC4EB8hfGmxoTk7PBrebc8AG7ZUdqjbTGu0nIhBh-54EH6icrfO2UdhPPJRFRvrfcinvrMe6z-LpCXFGhULeBDv1mmYeeXvSHqrYkJ6_r9pauhFcc2WdZgjFvpJ4YXtZEqLdmO-0asDxhPdT2ReCXdKs1gafyH_O-p8iETF5_uV_RtHcb4lDTkKCylOU1mlu2HO72FM5XUuiZRtMaZY9G3k2ti2bLmT9LGF1Qd4cTlvUaBFN-Tv0qWYnGSaQLov5OTlyVd5p8huVjrvxcRGviJG79n2rMl61wioP8l_FnfeXtbzsdA8Q3bnFmdtZCe7yvY11cCZ-Zk_iyBXT4bXQuaZzA3cqw_YkJH0TDqqxr-m_MbHvtqRxt-p6DgMNavmNCSLe_KavfkdAAD__w%3D%3D&sketch=0&theme=0&)

### Descrição das Tabelas

#### 1. Gerenciamento de Usuários
- **Tabela `users`**: Armazena informações sobre os usuários do sistema, integrada com o sistema de autenticação do Supabase. Essencial para gerenciar o acesso de diferentes perfis de usuários, como pesquisadores e técnicos.

#### 2. Gerenciamento de Projetos
- **Tabela `projects`**: Contém os dados básicos dos projetos de inspeção, incluindo nome, descrição e endereço. Esta tabela suporta a organização de múltiplas inspeções por edificação.
- **Tabela `user_projects`**: Estabelece relação N-N entre usuários e projetos, permitindo colaboração entre diferentes profissionais.

#### 3. Gerenciamento de Imagens
- **Tabela `images`**: Armazena metadados das imagens capturadas, incluindo informações sobre o arquivo, edificação (eixo, andar) e atributos técnicos. Esta estrutura facilita a organização e recuperação eficiente das imagens, além do melhor processamento da IA com a questão do eixo da foto e andar.

#### 4. Resultados de Análises
- **Tabela `results`**: Registra os resultados das análises de IA, incluindo confiabilidade (trustability), severidade e tipo da fissura detectada.
- **Tabela `project_results`**: Associa resultados de análises a projetos específicos, permitindo a visualização agregada de problemas por projeto.

#### 5. Relatórios
- **Tabela `reports`**: Contém os metadados dos relatórios gerados, incluindo caminho do arquivo e data de geração.
- **Tabela `reports_images`**: Estabelece relações entre relatórios e as imagens incluídas, facilitando a rastreabilidade dos dados e análises.

#### 6. Armazenamento
- Buckets de armazenamento para imagens de fissuras e relatórios gerados, garantindo organização e segurança dos arquivos.

## Implementação Técnica

A implementação do banco de dados no Supabase incluiu diversas características técnicas essenciais para garantir segurança, eficiência e integridade dos dados:

### 1. Integração com Sistema de Autenticação

O banco de dados está integrado com o sistema de autenticação nativo do Supabase através de triggers que sincronizam automaticamente os usuários:

```sql
CREATE OR REPLACE FUNCTION public.handle_new_user() 
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.users (id, email, name, created_at)
  VALUES (new.id, new.email, new.raw_user_meta_data->>'name', new.created_at);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
```

Esta integração garante consistência entre o sistema de autenticação e a tabela de usuários personalizada do banco de dados.

### 2. Segurança com Row Level Security (RLS)

Foram implementadas RLS's para as tabelas, garantindo que usuários tenham acesso apenas aos dados que estão associados:

```sql
-- Exemplo de políticas RLS para projetos
CREATE POLICY "Usuários podem ver seus projetos" ON projects
  FOR SELECT USING (
    id IN (
      SELECT project_id FROM user_projects WHERE user_id = auth.uid()
    )
  );
```

### 3. Otimização de Performance

Foram criados índices estratégicos para melhorar o desempenho das consultas mais frequentes, atendendo à necessidade de agilidade identificada para o perfil técnico.:

```sql
CREATE INDEX idx_user_projects_user ON user_projects(user_id);
CREATE INDEX idx_user_projects_project ON user_projects(project_id);
CREATE INDEX idx_images_project ON images(project_id);
CREATE INDEX idx_reports_project ON reports(project_id);
CREATE INDEX idx_reports_result ON reports(result_id);
CREATE INDEX idx_project_results_project ON project_results(project_id);
```

### 4. Armazenamento de Arquivos

Foram configurados buckets específicos para armazenamento de imagens e relatórios:

```sql
INSERT INTO storage.buckets (id, name, public)
VALUES 
  ('crack_images', 'Imagens de Fissuras', false),
  ('reports', 'Relatórios', false)
ON CONFLICT DO NOTHING;
```

As políticas de acesso a estes buckets garantem que usuários possam acessar apenas seus próprios arquivos:

```sql
CREATE POLICY "Acesso de usuários às suas imagens" ON storage.objects
  FOR SELECT USING (
    bucket_id = 'crack_images' AND 
    (auth.uid() IS NOT NULL) AND
    (position(auth.uid()::text in name) > 0)
  );
```

## Alinhamento com a Interface e Fluxo do Sistema

A estrutura do banco de dados foi projetada para suportar as funcionalidades apresentadas no [protótipo de alta fidelidade](LINK_PARA_PROTOTIPO) do sistema, garantindo que todas as interações do usuário sejam devidamente persistidas:

1. **Login e Cadastro**: Suportados pela tabela `users` e integração com autenticação
2. **Upload de Imagens**: Implementado através da tabela `images` e bucket de armazenamento
3. **Seleção de Modelo de IA**: Os resultados das análises são registrados na tabela `results`
4. **Auditoria de Imagens**: O campo `trustability` na tabela `results` permite identificar análises com baixa confiabilidade (abaixo de 75%) que necessitam revisão humana
5. **Insights e Relatórios**: Suportados pelas tabelas `reports`, `reports_images` e relações com resultados
6. **Histórico de Relatórios**: A estrutura temporal com timestamps permite acompanhamento cronológico de todas as análises e relatórios

Esta estrutura também se integra com a [arquitetura do sistema](LINK_PARA_ARQUITETURA), principalmente no que se refere ao fluxo de dados entre os módulos de captura, processamento por IA, e visualização dos resultados.

## Conclusão

O banco de dados implementado para o Sistema Óptico de Detecção fornece uma base sólida para todas as operações do sistema, desde o armazenamento seguro de imagens até a geração e persistência de relatórios técnicos detalhados. A estrutura foi cuidadosamente planejada para atender tanto às necessidades de rigor científico da pesquisadora Mariana quanto às necessidades de praticidade operacional do técnico Carlos, personas do projeto.