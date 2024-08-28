import asyncio

async def create_user(name, age):
    user = await objects.create(User, name=name, age=age)
    return user

async def get_user(user_id):
    user = await objects.get(User, id=user_id)
    return user

async def update_user(user_id, name=None, age=None):
    user = await objects.get(User, id=user_id)
    if name:
        user.name = name
    if age:
        user.age = age
    user.updated_at = datetime.datetime.now()
    await objects.update(user)
    return user

async def delete_user(user_id):
    user = await objects.get(User, id=user_id)
    user.deleted_at = datetime.datetime.now()
    await objects.update(user)
    return user

async def main():
    # 创建用户
    user = await create_user('zhangsan', 88)
    print(f"Created user: {user.name}, age: {user.age}")

    # 获取用户
    user = await get_user(user.id)
    print(f"Retrieved user: {user.name}, age: {user.age}")

    # 更新用户
    user = await update_user(user.id, name='lisi')
    print(f"Updated user: {user.name}, age: {user.age}")

    # 删除用户
    user = await delete_user(user.id)
    print(f"Deleted user: {user.name}, age: {user.age}")

# 运行异步主函数
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())